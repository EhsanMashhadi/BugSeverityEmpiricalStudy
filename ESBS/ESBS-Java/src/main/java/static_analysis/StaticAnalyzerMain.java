package static_analysis;

import data.metric_extractor.MetricCalculatorMain;
import de.siegmar.fastcsv.writer.CsvWriter;
import data.method_extractor.BugsJarBug;
import data.method_extractor.D4JBug;
import data.method_extractor.Method;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.List;

public class StaticAnalyzerMain {
    public static void main(String[] args) throws IOException {
        analyzeSpotBugsD4J();
//        analyzeSpotBugsBugsJar();
    }

    private static void analyzeSpotBugsD4J() throws IOException {
        AnalyzerFactory analyzerFactory = new AnalyzerFactory();
        StaticAnalyzer spotBugsAnalyzer = analyzerFactory.getAnalyzer(Analyzer.SPOTBUGS);

        String reportBase = "/home/ehsan/Workspace/java/ESBS/ESBS-Python/data/spotbugs/d4j/";

        List<Method> buggyMethods = MetricCalculatorMain.readD4JBuggyMethods();
        List<Method> nonBuggyMethods = MetricCalculatorMain.readD4JNonBuggyMethods();
        List<Method> foundBuggyMethods = spotBugsAnalyzer.analyze(buggyMethods, reportBase);
        List<Method> foundNonbuggyMethods = spotBugsAnalyzer.analyze(nonBuggyMethods, reportBase);

        CsvWriter csvWriter = CsvWriter.builder().build(Paths.get("d4j_spotbugs_found.csv"));
        csvWriter.writeRow("ProjectName", "ProjectVersion", "IssueTracker", "URL", "Priority", "ClassName", "StartLine", "EndLine", "Rank", "PrioritySpotBugs", "SourceCode");

        for (Method method : foundBuggyMethods) {
            D4JBug bug = (D4JBug) method.getRelatedBug();
            csvWriter.writeRow(method.getRelatedBug().getProjectName(), bug.getProjectVersion(), bug.getIssueTracker(), bug.getUrl(), bug.getSeverity(), method.getFileName(), "" + method.getStartLine(), "" + method.getEndLine(), method.getStaticResult().getRank(), method.getStaticResult().getConfidence(), method.getMethodString());
        }
        csvWriter.close();
    }

    private static void analyzeSpotBugsBugsJar() throws IOException {
        AnalyzerFactory analyzerFactory = new AnalyzerFactory();
        String reportBase = "/home/ehsan/Workspace/java/ESBS/ESBS-Python/data/spotbugs/bugs_jar/";
        StaticAnalyzer spotBugsAnalyzer = analyzerFactory.getAnalyzer(Analyzer.SPOTBUGS);

        List<Method> buggyMethods = MetricCalculatorMain.readBugsJarBuggyMethods();
        List<Method> nonBuggyMethods = MetricCalculatorMain.readBugsJarNonBuggyMethods();

        List<Method> foundBuggyMethods = spotBugsAnalyzer.analyze(buggyMethods, reportBase);
        List<Method> foundNonbuggyMethods = spotBugsAnalyzer.analyze(nonBuggyMethods, reportBase);

        CsvWriter csvWriter = CsvWriter.builder().build(Paths.get("bugsjar_spotbugs_found.csv"));
        csvWriter.writeRow("ProjectName", "ProjectVersion", "Priority", "ClassName", "StartLine", "EndLine", "Rank", "PrioritySpotBugs", "SourceCode");

        for (Method method : foundBuggyMethods) {
            BugsJarBug bug = (BugsJarBug) method.getRelatedBug();
            csvWriter.writeRow(method.getRelatedBug().getProjectName(), bug.getProjectVersion(), bug.getSeverity(), method.getFileName(), "" + method.getStartLine(), "" + method.getEndLine(), method.getStaticResult().getRank(), method.getStaticResult().getConfidence(), method.getMethodString());
        }
        csvWriter.close();
    }

    private static void analyzeInferD4J() {
        //        spotBugsAnalyzer = analyzerFactory.getAnalyzer(Analyzer.INFER);
//        String inferBasePath = "/home/ehsan/Workspace/java/ESBS/ESBS-Python/data/infer";
//        spotBugsAnalyzer.analyze(buggyMethods,inferBasePath);
//        spotBugsAnalyzer.analyze(nonBuggyMethods,inferBasePath);

    }
}
