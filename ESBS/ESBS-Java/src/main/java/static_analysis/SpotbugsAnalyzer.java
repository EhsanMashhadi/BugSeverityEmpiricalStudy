package static_analysis;


import com.github.javaparser.JavaParser;
import com.github.javaparser.ast.body.MethodDeclaration;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;
import data.method_extractor.BugsJarBug;
import data.method_extractor.D4JBug;
import data.method_extractor.Method;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class SpotbugsAnalyzer implements StaticAnalyzer {

//    public List<Method> analyze(List<Method> methods, String reportFile) {
//        AtomicInteger nullSourceLine = new AtomicInteger();
//        AtomicBoolean found = new AtomicBoolean(false);
//
//        AtomicInteger notFoundCount = new AtomicInteger();
//        AtomicInteger foundCount = new AtomicInteger();
//
//        List<Method> foundMethods = new ArrayList<>();
//        List<Method> notFoundMethods = new ArrayList<>();
//
//        methods.parallelStream().forEach(method -> {
//            found.set(false);
//            String fileName = "";
//            String projectName = "";
//            String projectVersion = "";
//
//            if (method.getRelatedBug().getClass() == D4JBug.class) {
//                projectName = method.getRelatedBug().getProjectName();
//                projectVersion = ((D4JBug) method.getRelatedBug()).getProjectVersion();
//                fileName = String.format(reportFile + "%s%sb.xml", projectName, projectVersion);
//            } else if (method.getRelatedBug().getClass() == BugsJarBug.class) {
//                projectName = method.getRelatedBug().getProjectName();
//                projectVersion = ((BugsJarBug) method.getRelatedBug()).getBranchName();
//                projectVersion = projectVersion.substring(projectVersion.lastIndexOf("/") + 1);
//                fileName = String.format(reportFile + "%s_%s.xml", projectName, projectVersion);
//            }
//
//            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
//            NodeList bugs = null;
//            try {
//                DocumentBuilder builder = factory.newDocumentBuilder();
//                File file = new File(fileName);
//                if (!file.exists()) {
//                    System.err.println("No Report Found " + projectName + " " + projectVersion);
//                    return;
//                }
//                Document document = builder.parse(file);
//                document.getDocumentElement().normalize();
//                bugs = document.getElementsByTagName("BugInstance");
//            } catch (ParserConfigurationException | IOException | SAXException e) {
//                e.printStackTrace();
//            }
//
//            System.out.println(fileName);
//
//            MethodDeclaration methodDeclaration = JavaParser.parseBodyDeclaration(method.getMethodString()).asMethodDeclaration();
//
//            for (int i = 0; i < bugs.getLength(); i++) {
//                Node node = bugs.item(i);
//                if (node.getNodeType() == Node.ELEMENT_NODE) {
//                    String rank = node.getAttributes().getNamedItem("rank").getNodeValue();
//                    String confidence = node.getAttributes().getNamedItem("priority").getNodeValue();
//                    Element eElement = (Element) node;
//                    NodeList detectedMethods = eElement.getElementsByTagName("Method");
//                    for (int j = 0; j < detectedMethods.getLength(); j++) {
//                        Node detectedMethod = detectedMethods.item(j);
//                        Element methodElement = (Element) detectedMethod;
//                        String methodName = methodElement.getAttributes().getNamedItem("name").getNodeValue();
////                        String methodSignature = methodElement.getAttributes().getNamedItem("signature").getNodeValue();
//                        String methodClassName = methodElement.getAttributes().getNamedItem("classname").getNodeValue();
//
//                        Node sourceLine = methodElement.getElementsByTagName("SourceLine").item(0);
//
//                        if (method.getFileName().replace("/", ".").contains(methodClassName)) {
//                            int methodStartLine = -1;
////                            int methodEndLine = -1;
//                            if (sourceLine != null) {
//                                nullSourceLine.addAndGet(1);
//                                if (sourceLine.getAttributes().getNamedItem("start") != null) {
//                                    methodStartLine = Integer.parseInt(sourceLine.getAttributes().getNamedItem("start").getNodeValue());
//                                }
//
////                                if (sourceLine.getAttributes().getNamedItem("end") != null) {
////                                    methodEndLine = Integer.parseInt(sourceLine.getAttributes().getNamedItem("end").getNodeValue());
////                                }
//                                if (methodName.equals(methodDeclaration.getNameAsString()) || (methodStartLine >= method.getStartLine() - 2 && methodStartLine <= method.getStartLine() + 2)) {
//                                    foundCount.addAndGet(1);
////                                    System.out.println("Found!!!!!");
////                                    System.out.println("Method Name: " + methodName);
////                                    System.out.println("Method Signature: " + methodSignature);
////                                    System.out.println();
////                                    method.setStaticResult(new StaticResult(rank, confidence));
////                                    foundMethods.add(method);
//                                    found.set(true);
//                                }
//                            }
//                        }
//                    }
//                }
//            }
//            if (!found.get()) {
////                notFoundMethods.add(method);
//                notFoundCount.addAndGet(1);
//            }
//        });
//
//
//        Set<Method> uniqueFound = new HashSet<Method>(foundMethods);
//        Set<Method> uniqueNotFound = new HashSet<Method>(notFoundMethods);
//
//        System.out.println("Total Method Found: " + foundCount);
//        System.out.println("Unique Method Found: " + uniqueFound.size());
//        System.out.println("Total Method Not Found: " + notFoundCount);
//        System.out.println("Unique Method Not Found: " + uniqueNotFound.size());
//        System.out.println("Count of null source line: " + nullSourceLine);
//
//        return foundMethods;
//
//    }

    public List<Method> analyze(List<Method> methods, String reportFile) {
        boolean found = false;

        int notFoundCount = 0;
        int foundCount = 0;

        List<Method> foundMethods = new ArrayList<>();
        List<Method> notFoundMethods = new ArrayList<>();


        for (Method method : methods) {
            found = false;
            String fileName = "";
            String projectName = "";
            String projectVersion = "";

            if (method.getRelatedBug().getClass() == D4JBug.class) {
                projectName = method.getRelatedBug().getProjectName();
                projectVersion = ((D4JBug) method.getRelatedBug()).getProjectVersion();
                fileName = String.format(reportFile + "%s%sb.xml", projectName, projectVersion);
            } else if (method.getRelatedBug().getClass() == BugsJarBug.class) {
                projectName = method.getRelatedBug().getProjectName();
                projectVersion = ((BugsJarBug) method.getRelatedBug()).getProjectVersion();
                projectVersion = projectVersion.substring(projectVersion.lastIndexOf("/") + 1);
                fileName = String.format(reportFile + "%s_%s.xml", projectName, projectVersion);

            }

            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            NodeList bugs = null;
            try {
                DocumentBuilder builder = factory.newDocumentBuilder();
                File file = new File(fileName);
                if (!file.exists()) {
                    System.err.println("No Report Found: " + projectName + " " + projectVersion);
                    continue;
                }
                Document document = builder.parse(file);
                document.getDocumentElement().normalize();
                bugs = document.getElementsByTagName("BugInstance");
            } catch (ParserConfigurationException | IOException | SAXException e) {
                e.printStackTrace();
            }

            System.out.println("Working on: " + fileName);

            MethodDeclaration methodDeclaration = JavaParser.parseBodyDeclaration(method.getMethodString()).asMethodDeclaration();

            for (int i = 0; i < bugs.getLength(); i++) {
                Node node = bugs.item(i);
                if (node.getNodeType() == Node.ELEMENT_NODE) {
                    String rank = node.getAttributes().getNamedItem("rank").getNodeValue();
                    String confidence = node.getAttributes().getNamedItem("priority").getNodeValue();
                    Element eElement = (Element) node;
                    NodeList detectedMethods = eElement.getElementsByTagName("Method");
                    for (int j = 0; j < detectedMethods.getLength(); j++) {
                        Node detectedMethod = detectedMethods.item(j);
                        Element methodElement = (Element) detectedMethod;
                        String methodName = methodElement.getAttributes().getNamedItem("name").getNodeValue();
                        String methodClassName = methodElement.getAttributes().getNamedItem("classname").getNodeValue();

                        Node sourceLine = methodElement.getElementsByTagName("SourceLine").item(0);

                        if (method.getFileName().replace("/", ".").contains(methodClassName)) {
                            int methodStartLine = -1;
                            if (sourceLine != null) {
                                if (sourceLine.getAttributes().getNamedItem("start") != null) {
                                    methodStartLine = Integer.parseInt(sourceLine.getAttributes().getNamedItem("start").getNodeValue());
                                }
                                if (methodName.equals(methodDeclaration.getNameAsString()) || (methodStartLine >= method.getStartLine() - 2 && methodStartLine <= method.getStartLine() + 2)) {
                                    foundCount += 1;
                                    method.setStaticResult(new StaticResult(rank, confidence));
                                    foundMethods.add(method);
                                    found = true;
                                }
                            }
                        }
                    }
                }
            }
            if (!found) {
                notFoundMethods.add(method);
                notFoundCount += 1;
            }
        }

        Set<Method> uniqueFound = new HashSet<>(foundMethods);
        Set<Method> uniqueNotFound = new HashSet<>(notFoundMethods);

        System.out.println("Total Method Found: " + foundCount);
        System.out.println("Unique Method Found: " + uniqueFound.size());
        System.out.println("Total Method Not Found: " + notFoundCount);
        System.out.println("Unique Method Not Found: " + uniqueNotFound.size());

        return foundMethods;
    }
}
