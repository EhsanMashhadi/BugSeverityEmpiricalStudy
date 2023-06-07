package static_analysis;

public class StaticResult {
    private String rank;
    private String confidence;

    public StaticResult(String rank, String confidence) {
        this.rank = rank;
        this.confidence = confidence;
    }

    public String getRank() {
        return rank;
    }

    public String getConfidence() {
        return confidence;
    }
}
