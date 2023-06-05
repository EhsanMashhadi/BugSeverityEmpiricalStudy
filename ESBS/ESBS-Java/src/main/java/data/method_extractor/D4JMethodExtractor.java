package data.method_extractor;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ast.body.MethodDeclaration;
import utils.GitUtil;

import java.io.File;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class D4JMethodExtractor implements MethodExtractor {

    @Override
    public List<List<Method>> extractMethods(List<Bug> bugs) {

        List<Method> buggyMethods = new ArrayList<>();
        List<Method> nonBuggyMethods = new ArrayList<>();
        List<Method> fixedMethods = new ArrayList<>();

        try {

            for (Bug bug : bugs) {

                D4JBug d4JBug = (D4JBug) bug;
                String projectName = d4JBug.getProjectName();
                String projectVersion = d4JBug.getProjectVersion();
                String priority = d4JBug.getSeverity();

                int buggyMethodsCountTemp = buggyMethods.size();
                int nonBuggyMethodsCountTemp = nonBuggyMethods.size();

                if (!priority.isEmpty()) {
                    String result = GitUtil.checkoutDJ4(projectName, projectVersion, true);
                    List<String> changedFiles = GitUtil.getD4JBuggyFiles(projectName, projectVersion);
                    String projectRepoBasePath = "/home/ehsan/Workspace/java/ESBS/ESBS-Python/data/projects_repo/";
                    for (String changedFile : changedFiles) {
                        String result1 = GitUtil.checkoutDJ4(projectName, projectVersion, true);
                        Path path = Paths.get(projectRepoBasePath, projectName + projectVersion + "b", changedFile);
                        File file = new File(path.toUri());
                        if (!file.exists()) {
                            System.err.println("Java File NOT FOUND!!!");
                            System.err.println("ProjectName: " + projectName);
                            System.err.println("Project Branch: " + projectVersion);
                            System.err.println();
                            continue;
                        }
                        List<MethodDeclaration> buggyFileMethods = JavaParser.parse(path).findAll(MethodDeclaration.class);
                        GitUtil.checkoutDJ4(projectName, projectVersion, false);
                        List<MethodDeclaration> fixedFileMethods = JavaParser.parse(path).findAll(MethodDeclaration.class);
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
                        System.err.println("Project Branch: " + projectVersion);
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