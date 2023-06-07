package static_analysis;

public class AnalyzerFactory {

    public StaticAnalyzer getAnalyzer(Analyzer analyzer) {
        switch (analyzer) {
            case SPOTBUGS:
                return new SpotbugsAnalyzer();
            case INFER:
                return new InferAnalyzer();
        }
        throw new RuntimeException();
    }
}
