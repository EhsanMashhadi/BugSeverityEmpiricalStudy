package static_analysis;


import data.method_extractor.Method;

import java.io.IOException;
import java.util.List;

public interface StaticAnalyzer {
    List<Method> analyze(List<Method> buggyMethods, String reportFile) throws IOException;
}
