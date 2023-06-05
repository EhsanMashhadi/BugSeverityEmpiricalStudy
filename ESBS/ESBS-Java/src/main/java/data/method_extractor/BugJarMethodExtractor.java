package data.method_extractor;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ast.body.MethodDeclaration;
import utils.GitUtil;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class BugJarMethodExtractor implements MethodExtractor {

    @Override
    public List<List<Method>> extractMethods(List<Bug> bugs) {

        List<Method> buggyMethods = new ArrayList<>();
        List<Method> nonBuggyMethods = new ArrayList<>();
        List<Method> fixedMethods = new ArrayList<>();

        try {
            for (Bug bug : bugs) {

                BugsJarBug bugsJarBug = (BugsJarBug) bug;
                String projectName = bugsJarBug.getProjectName();
                String branchName = bugsJarBug.getProjectVersion();
                String priority = bugsJarBug.getSeverity();

                int buggyMethodsCountTemp = buggyMethods.size();
                int nonBuggyMethodsCountTemp = nonBuggyMethods.size();

                if (!priority.isEmpty()) {
                    String result = GitUtil.checkoutBugsJar(projectName, branchName, true);
                    List<String> changedFiles = GitUtil.getBugsJarBuggyFiles(projectName, branchName);
                    String projectRepoBasePath = "/home/ehsan/Workspace/java/bugsjar/bugs-dot-jar/";
                    for (String changedFile : changedFiles) {
                        String result1 = GitUtil.checkoutBugsJar(projectName, branchName, true);
                        List<MethodDeclaration> buggyFileMethods = JavaParser.parse(Paths.get(projectRepoBasePath, projectName, changedFile)).findAll(MethodDeclaration.class);
                        GitUtil.checkoutBugsJar(projectName, branchName, false);
                        List<MethodDeclaration> fixedFileMethods = JavaParser.parse(Paths.get(projectRepoBasePath, projectName, changedFile)).findAll(MethodDeclaration.class);
                        for (MethodDeclaration suspiciousMethod : buggyFileMethods) {
                            if (!fixedFileMethods.contains(suspiciousMethod)) {
                                buggyMethods.add(new Method(true, bug, changedFile, suspiciousMethod.getBegin().get().line, suspiciousMethod.getEnd().get().line, suspiciousMethod.toString()));
                            } else {
                                nonBuggyMethods.add(new Method(false, bug, changedFile, suspiciousMethod.getBegin().get().line, suspiciousMethod.getEnd().get().line, suspiciousMethod.toString()));
                            }
                        }

                        for (MethodDeclaration fixedMethod : fixedFileMethods) {
                            if (!buggyFileMethods.contains(fixedMethod)) {
                                fixedMethods.add(new Method(false, bug, changedFile, fixedMethod.getBegin().get().line, fixedMethod.getEnd().get().line, fixedMethod.toString()));
                            }
                        }
                    }
                    System.out.println("Changed Class Count: " + changedFiles.size());
                    System.out.println("Buggy Methods Count: " + (buggyMethods.size() - buggyMethodsCountTemp));
                    System.out.println("Non-buggy Methods Count: " + (nonBuggyMethods.size() - nonBuggyMethodsCountTemp));
                    System.out.println();

                    if (buggyMethodsCountTemp == buggyMethods.size()) {
                        System.err.println("ERROR ZERO");
                        System.err.println("ProjectName: " + projectName);
                        System.err.println("Project Branch: " + branchName);
                        for (String className : changedFiles) {
                            System.err.println("ClassName: " + className);
                        }
                        System.err.println();
                    }

                }
            }
            ArrayList<List<Method>> methods = new ArrayList<>();
            methods.add(buggyMethods);
            methods.add(nonBuggyMethods);
            methods.add(fixedMethods);
            return methods;

        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }
}
