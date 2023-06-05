package data.method_extractor;

import metrics.CodeMetrics;
import static_analysis.StaticResult;

public class Method {

    private Bug relatedBug;
    private String fileName;
    private int startLine;
    private int endLine;
    private String methodString;
    private CodeMetrics codeMetrics;
    private boolean isBuggy;
    private StaticResult staticResult;

    public Method(boolean isBuggy, Bug relatedBug, String fileName, int startLine, int endLine, String methodString) {
        this.isBuggy = isBuggy;
        this.relatedBug = relatedBug;
        this.fileName = fileName;
        this.startLine = startLine;
        this.endLine = endLine;
        this.methodString = methodString;
    }

    public void setCodeMetrics(CodeMetrics codeMetrics) {
        this.codeMetrics = codeMetrics;
    }

    public CodeMetrics getCodeMetrics() {
        return codeMetrics;
    }

    public Bug getRelatedBug() {
        return relatedBug;
    }

    public String getFileName() {
        return fileName;
    }

    public int getStartLine() {
        return startLine;
    }

    public int getEndLine() {
        return endLine;
    }

    public String getMethodString() {
        return methodString;
    }

    public boolean isBuggy() {
        return isBuggy;
    }

    public void setStaticResult(StaticResult staticResult) {
        this.staticResult = staticResult;
    }

    public StaticResult getStaticResult() {
        return staticResult;
    }
}
