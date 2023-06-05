package data.method_extractor;

import java.util.List;

public interface MethodExtractor {
    List<List<Method>> extractMethods(List<Bug> bugs);
}
