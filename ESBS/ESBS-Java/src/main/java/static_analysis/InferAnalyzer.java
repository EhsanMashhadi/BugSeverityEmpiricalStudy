package static_analysis;

import org.json.JSONArray;
import org.json.JSONObject;
import data.method_extractor.D4JBug;
import data.method_extractor.Method;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class InferAnalyzer implements StaticAnalyzer {


//    public void analyzeReportD4j() throws IOException {
//        CsvWriter csvWriter = CsvWriter.builder().build(Paths.get("d4j_infer_found.csv"));
//        csvWriter.writeRow("ProjectName", "ProjectVersion", "IssueTracker", "URL", "Priority", "ClassName", "StartLine", "EndLine", "Severity", "SourceCode");
//
//        CsvReader csvReader = CsvReader.builder().build(Paths.get("/home/ehsan/Workspace/java/ESBS/d4j_methods_buggy.csv"));
//        CloseableIterator<CsvRow> csvRow = csvReader.iterator();
//        csvRow.next();
//        int totalFound = 0;
//        int totalNotFound = 0;
//        int nullSourceLine = 0;
//        int totalBuggyMethodFound = 0;
//
//        while (csvRow.hasNext()) {
//            boolean found = false;
//            CsvRow myRow = csvRow.next();
//            String projectName = myRow.getField(0);
//            String projectVersion = myRow.getField(1);
//            String issueTracker = myRow.getField(2);
//            String url = myRow.getField(3);
//            String priority = myRow.getField(4);
//            String className = myRow.getField(5);
//            int startLine = Integer.parseInt(myRow.getField(6));
//            int endLine = Integer.parseInt(myRow.getField(7));
//            String sourceCode = myRow.getField(8);
//
//            String fileName = String.format("/home/ehsan/Workspace/java/ESBS/ESBS-Python/data/infer/%s%sb/report.json", projectName, projectVersion);
//
//            Path report_file = Paths.get(fileName);
//            File file = new File(report_file.toUri());
//            if (!file.exists())
//                continue;
//            String jsonReport = new String(Files.readAllBytes(Paths.get(fileName)));
//            JSONArray bugs = new JSONArray(jsonReport);
//            System.out.println(fileName);
//
//            for (int i = 0; i < bugs.length(); i++) {
//                JSONObject node = bugs.getJSONObject(i);
//                String inferPriority = node.getString("severity");
//                int sourceLine = node.getInt("line");
//
//                System.out.println(inferPriority);
//                System.out.println(sourceLine);
//
//                if (sourceLine >= startLine && sourceLine <= endLine) {
//                    found = true;
//                    totalFound += 1;
//                    csvWriter.writeRow(projectName, projectVersion, issueTracker, url, priority, className, "" + startLine, "" + endLine, inferPriority, sourceCode);
//                }
//            }
//
//            if (!found) {
//                totalNotFound += 1;
//            }
//
//        }
//
//        System.out.println("Total found");
//        System.out.println(totalFound);
//        System.out.println("Total No Found:" + totalNotFound);
//        System.out.println("null source line");
//        System.out.println(nullSourceLine);
//        System.out.println("Total spotbugs found");
//        System.out.println(totalBuggyMethodFound);
//
//        csvReader.close();
//        csvWriter.close();
//    }

    @Override
    public List<Method> analyze(List<Method> buggyMethods, String reportFile) throws IOException {

        int totalFound = 0;
        int totalNotFound = 0;
        int nullSourceLine = 0;

        List<Method> foundMethods = new ArrayList<>();
        List<Method> notFoundMethods = new ArrayList<>();


        for (Method method : buggyMethods) {
            boolean found = false;
            String fileName = "";
            String projectName = "";
            String projectVersion = "";

            if (method.getRelatedBug().getClass() == D4JBug.class) {
                projectName = method.getRelatedBug().getProjectName();
                projectVersion = ((D4JBug) method.getRelatedBug()).getProjectVersion();
                fileName = String.format(reportFile + "/%s%sb/report.json", projectName, projectVersion);
            }

            Path report_file = Paths.get(fileName);
            File file = new File(report_file.toUri());
            if (!file.exists())
                continue;
            String jsonReport = new String(Files.readAllBytes(Paths.get(fileName)));
            JSONArray bugs = new JSONArray(jsonReport);
            System.out.println(fileName);

            for (int i = 0; i < bugs.length(); i++) {
                JSONObject node = bugs.getJSONObject(i);
                String inferPriority = node.getString("severity");
                int sourceLine = node.getInt("line");

                if (sourceLine >= method.getStartLine() && sourceLine <= method.getEndLine()) {
                    System.out.println("Found");
                    found = true;
                    totalFound += 1;
                    foundMethods.add(method);
                }
            }

            if (!found) {
                totalNotFound += 1;
                notFoundMethods.add(method);
            }

        }
        Set<Method> uniqueFound = new HashSet<>(foundMethods);
        Set<Method> uniqueNotFound = new HashSet<>(notFoundMethods);

        System.out.println("Total found: " + totalFound);
        System.out.println("Unique found: " + uniqueFound.size());
        System.out.println("Total Not Found:" + totalNotFound);
        System.out.println("Unique Not found: " + uniqueNotFound.size());
        System.out.println("Null source line: " + nullSourceLine);
        return null;

    }

}
