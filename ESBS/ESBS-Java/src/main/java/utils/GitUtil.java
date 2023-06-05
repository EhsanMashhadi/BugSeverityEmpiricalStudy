package utils;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class GitUtil {

    public static String checkoutBugsJar(String projectName, String branchName, boolean buggy) throws IOException {
        //update scripts to download bugs.jar into data folder in python module and use that path instead of this path
        String command = "";
        if (buggy) {
            command = "git checkout " + branchName;
        } else {
            command = "git checkout " + branchName.split("_")[branchName.split("_").length - 1];
        }
        String projectRepoBasePath = "/home/ehsan/Workspace/java/bugsjar/bugs-dot-jar/";
        return runCommand(command, projectRepoBasePath, projectName);
    }

    public static String checkoutDJ4(String projectName, String projectVersion, boolean buggy) throws IOException {
        String command = "";
        if (buggy) {
            command = "git checkout " + "D4J_" + projectName + "_" + projectVersion + "_BUGGY_VERSION";
        } else {
            command = "git checkout " + "D4J_" + projectName + "_" + projectVersion + "_FIXED_VERSION";
        }
        String projectRepoBasePath = "/home/ehsan/Workspace/java/ESBS/ESBS-Python/data/projects_repo/";
        return runCommand(command, projectRepoBasePath, projectName + projectVersion + "b");
    }

    private static String runCommand(String command, String projectRepoBasePath, String projectName) throws IOException {
        Process process = Runtime.getRuntime().exec(command, null, new File(projectRepoBasePath, projectName));
        StringBuilder result = new StringBuilder();
        BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream()));
        String inputLine;
        while ((inputLine = in.readLine()) != null) {
            result.append(inputLine);
        }
        in.close();
        return result.toString();
    }

    public static Map<String, List<String>> getModifiedLines(String projectName, String branchName) throws IOException {
        Map<String, List<String>> changes = new HashMap<>();
        String toDiff = branchName.split("_")[branchName.split("_").length - 1];
        String[] command = {"/bin/sh", "-c", "git diff " + toDiff + " --unified=0 | grep -Po '^\\+\\+\\+ ./\\K.*|^@@ -[0-9]+(,[0-9]+)? \\+\\K[0-9]+(,[0-9]+)?(?= @@)'"};
        String projectRepoBasePath = "/home/ehsan/Workspace/java/bugsjar/bugs-dot-jar/";
        Process process = Runtime.getRuntime().exec(command, null, new File(projectRepoBasePath, projectName));
        BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream()));
        String inputLine;
        String myKey = "";
        while ((inputLine = in.readLine()) != null) {
            if (inputLine.endsWith(".java")) {
                myKey = inputLine;
                continue;
            }
            if (!myKey.isEmpty()) {
                List<String> value = changes.getOrDefault(myKey, new ArrayList<>());
                value.add(inputLine);
                changes.put(myKey, value);
            }
        }
        in.close();
        return changes;
    }


    public static List<String> getBugsJarBuggyFiles(String projectName, String branchName) throws IOException {

        String command = "git diff " + branchName.split("_")[branchName.split("_").length - 1] + " --name-only";
        String projectRepoBasePath = "/home/ehsan/Workspace/java/bugsjar/bugs-dot-jar/";
        return getChangedFiles(command, projectRepoBasePath, projectName);
    }

    public static List<String> getD4JBuggyFiles(String projectName, String projectVersion) throws IOException {
        String command = "git diff " + "D4J_" + projectName + "_" + projectVersion + "_FIXED_VERSION" + " --name-only";
        String projectRepoBasePath = "/home/ehsan/Workspace/java/ESBS/ESBS-Python/data/projects_repo/";
        return getChangedFiles(command, projectRepoBasePath, projectName + projectVersion + "b");
    }

    private static List<String> getChangedFiles(String command, String projectRepoBasePath, String projectName) throws IOException {
        Process process = Runtime.getRuntime().exec(command, null, new File(projectRepoBasePath, projectName));
        List<String> result = new ArrayList<>();
        BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream()));
        String inputLine;
        while ((inputLine = in.readLine()) != null) {
            if (inputLine.endsWith(".java")) {
                result.add(inputLine);
            }
        }
        in.close();
        return result;
    }
}
