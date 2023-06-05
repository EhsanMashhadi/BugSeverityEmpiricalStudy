package utils;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;

public class Defects4JUtil {

    public String getProjectSrcFolder(String projectName, String projectVersion) throws IOException {
        String projectRepoBasePath = "/home/ehsan/Workspace/java/ESBS/ESBS-Python/data/projects_repo/";
        String repoFolder = projectName + projectVersion + "b";
        String command = "defects4j export -p dir.src.classes";
        Process process = Runtime.getRuntime().exec(command, null, new File(projectRepoBasePath, repoFolder));
        StringBuilder result = new StringBuilder();
        BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream()));
        String inputLine;
        while ((inputLine = in.readLine()) != null) {
            result.append(inputLine);
        }
        in.close();
        return result.toString();
    }



    public static void main(String[] args) throws IOException {
        Defects4JUtil defects4J = new Defects4JUtil();
        String sourceFolder = defects4J.getProjectSrcFolder("Chart","2");
        System.out.println(sourceFolder);
    }
}
