package data.metric_extractor;

import data.method_extractor.BugsJarBug;
import data.method_extractor.D4JBug;
import data.method_extractor.Method;
import de.siegmar.fastcsv.reader.CloseableIterator;
import de.siegmar.fastcsv.reader.CsvReader;
import de.siegmar.fastcsv.reader.CsvRow;
import de.siegmar.fastcsv.writer.CsvWriter;
import metrics.CodeMetrics;
import utils.Constants;

import java.io.FileWriter;
import java.io.IOException;
import java.net.URISyntaxException;
import java.nio.file.Paths;
import java.text.DecimalFormat;
import java.util.List;
import java.util.stream.Collectors;

public class MetricCalculatorMain {
    private static final DecimalFormat df = new DecimalFormat("0.00");

    public static void main(String[] args) throws IOException, URISyntaxException {

        MetricCalculatorMain mainClass = new MetricCalculatorMain();
        mainClass.calcD4JCodeMetrics();
        mainClass.calcBugsJarCodeMetrics();
    }


    private void calcD4JCodeMetrics() throws IOException {

        List<Method> methods = readD4JMethods();
        CodeMetricCalculator codeMetricCalculator = new CodeMetricCalculator();
        codeMetricCalculator.setCodeMetrics(methods);
        writeD4JMetrics(methods);
    }


    private void calcBugsJarCodeMetrics() throws IOException {
        CodeMetricCalculator codeMetricCalculator = new CodeMetricCalculator();
        List<Method> methods = readBugsJarMethods();
        codeMetricCalculator.setCodeMetrics(methods);
        writeBugsJarMetrics(methods);
    }

    public static List<Method> readD4JBuggyMethods() throws IOException {
        String buggyPath = "/home/ehsan/Workspace/java/ESBS/d4j_methods_buggy.csv";

        CsvReader csvReader = CsvReader.builder().build(Paths.get(buggyPath));
        CloseableIterator<CsvRow> csvRow = csvReader.iterator();
        csvRow.next();
//        ProjectName, ProjectVersion, IssueTracker, URL, Priority, ClassName, StartLine, EndLine, SourceCode
        List<Method> methods = csvReader.stream().map(row -> new Method(true, new D4JBug(row.getField(0),
                row.getField(1), row.getField(2), row.getField(3), row.getField(4)),
                row.getField(5), Integer.parseInt(row.getField(6)), Integer.parseInt(row.getField(7)),
                row.getField(8))).collect(Collectors.toList());
        csvRow.close();
        return methods;
    }

    public static List<Method> readD4JNonBuggyMethods() throws IOException {
        String nonBuggyPath = "/home/ehsan/Workspace/java/ESBS/d4j_methods_nonbuggy.csv";

        CsvReader csvReader = CsvReader.builder().build(Paths.get(nonBuggyPath));
        CloseableIterator<CsvRow> csvRow = csvReader.iterator();
        csvRow.next();
//        ProjectName, ProjectVersion, IssueTracker, URL, Priority, ClassName, StartLine, EndLine, SourceCode
        List<Method> methods = csvReader.stream().map(row -> new Method(false, new D4JBug(row.getField(0),
                row.getField(1), row.getField(2), row.getField(3), row.getField(4)),
                row.getField(5), Integer.parseInt(row.getField(6)), Integer.parseInt(row.getField(7)),
                row.getField(8))).collect(Collectors.toList());
        return methods;
    }

    public static List<Method> readD4JMethods() throws IOException {
        List<Method> methods = readD4JBuggyMethods();
        methods.addAll(readD4JNonBuggyMethods());
        return methods;
    }

    private void writeD4JMetrics(List<Method> methods) throws IOException {
        String path = "d4j_methods_sc_metrics.csv";
        CsvWriter csvWriter = CsvWriter.builder().build(new FileWriter(path));
        String[] header = getMetricsFileHeader();
        csvWriter.writeRow(header);

        for (Method method : methods) {
            D4JBug d4JBug = (D4JBug) method.getRelatedBug();
            CodeMetrics codeMetrics = method.getCodeMetrics();
//            SLOC,IC,IC-NC,MCCABE,MCCABE-NC,NBD,MCCLURE,DIFF,MI,TFO,UFO,READABILITY
            csvWriter.writeRow(String.valueOf(method.isBuggy()), d4JBug.getProjectName(), d4JBug.getProjectVersion(),
                    d4JBug.getSeverity(), String.valueOf(method.getStartLine()), String.valueOf(method.getEndLine()),
                    df.format(codeMetrics.getSloc()), df.format(codeMetrics.getProxyIndentation()),
                    df.format(codeMetrics.getMcCabe()),
                    df.format(codeMetrics.getNestedBlockDepth()),
                    df.format(codeMetrics.getMcClure()), df.format(codeMetrics.getDifficulty()),
                    df.format(codeMetrics.getMaintainabilityIndex()), df.format(codeMetrics.getFanOut()),
                    df.format(codeMetrics.getReadability()), df.format(codeMetrics.getEffort()),
                    method.getMethodString());
        }
        csvWriter.close();
    }


    public static List<Method> readBugsJarMethods() throws IOException {
        List<Method> methods = readBugsJarBuggyMethods();
        methods.addAll(readBugsJarNonBuggyMethods());
        return methods;
    }

    public static List<Method> readBugsJarBuggyMethods() throws IOException {
        String path = "/home/ehsan/Workspace/java/ESBS/bugsjar_methods_buggy.csv";
        CsvReader csvReader = CsvReader.builder().build(Paths.get(path));
        CloseableIterator<CsvRow> csvRow = csvReader.iterator();
        csvRow.next();
        List<Method> methods = csvReader.stream().map(row -> new Method(true,
                new BugsJarBug(row.getField(0), row.getField(1), row.getField(2)),
                row.getField(3), Integer.parseInt(row.getField(4)), Integer.parseInt(row.getField(5)),
                row.getField(6))).collect(Collectors.toList());
        csvRow.close();
        return methods;
    }

    public static List<Method> readBugsJarNonBuggyMethods() throws IOException {
        String path = "/home/ehsan/Workspace/java/ESBS/bugsjar_methods_nonbuggy.csv";
        CsvReader csvReader = CsvReader.builder().build(Paths.get(path));
        CloseableIterator<CsvRow> csvRow = csvReader.iterator();
        csvRow.next();
        List<Method> methods = csvReader.stream().map(row -> new Method(false, new BugsJarBug(row.getField(0),
                row.getField(1), row.getField(2)), row.getField(3),
                Integer.parseInt(row.getField(4)), Integer.parseInt(row.getField(5)),
                row.getField(6))).collect(Collectors.toList());
        csvRow.close();
        return methods;
    }

    private void writeBugsJarMetrics(List<Method> methods) throws IOException {
        String path = "bugsjar_methods_sc_metrics.csv";
        CsvWriter csvWriter = CsvWriter.builder().build(new FileWriter(path));
        String[] metricHeader = getMetricsFileHeader();
        csvWriter.writeRow(metricHeader);
        for (Method method : methods) {
            BugsJarBug bugsJarBug = (BugsJarBug) method.getRelatedBug();
            CodeMetrics codeMetrics = method.getCodeMetrics();
//            SLOC,IC,IC-NC,MCCABE,MCCABE-NC,NBD,MCCLURE,DIFF,MI,TFO,UFO,READABILITY
            csvWriter.writeRow(String.valueOf(method.isBuggy()), bugsJarBug.getProjectName(), bugsJarBug.getProjectVersion(),
                    bugsJarBug.getSeverity(), String.valueOf(method.getStartLine()), String.valueOf(method.getEndLine()),
                    df.format(codeMetrics.getSloc()), df.format(codeMetrics.getProxyIndentation()),
                    df.format(codeMetrics.getMcCabe()),
                    df.format(codeMetrics.getNestedBlockDepth()),
                    df.format(codeMetrics.getMcClure()), df.format(codeMetrics.getDifficulty()),
                    df.format(codeMetrics.getMaintainabilityIndex()), df.format(codeMetrics.getFanOut()),
                    df.format(codeMetrics.getReadability()), df.format(codeMetrics.getEffort()), method.getMethodString());
        }
        csvWriter.close();
    }

    private String[] getMetricsFileHeader() {
        return new String[]{Constants.METHOD_IS_BUGGY_CSV_COL, Constants.PROJECT_NAME_CSV_COL, Constants.PROJECT_VERSION_CSV_COL,
                Constants.BUG_SEVERITY_CSV_COL, Constants.START_LINE_CSV_COL, Constants.END_LINE_CSV_COL, Constants.SLOC_COL, Constants.PROXY_INDENTATION_COL,
                Constants.MCCABE_COL,
                Constants.NESTED_BLOCK_DEPTH_COL, Constants.MCCLURE_COL, Constants.DIFFICULTY_COL,
                Constants.MAINTAINABILITY_COL, Constants.FAN_OUT_COL,
                Constants.READABILITY_COL, Constants.EFFORT_COL, Constants.SOURCE_CODE_CSV_COL};
    }
}