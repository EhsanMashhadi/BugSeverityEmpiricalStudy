package data.method_extractor;

public class Bug {
    private String projectName;
    private String severity;

    public Bug(String projectName, String severity) {
        this.projectName = projectName;
        this.severity = severity;
    }

    public String getProjectName() {
        return projectName;
    }

    public String getSeverity() {
        return severity;
    }
}
