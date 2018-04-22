#include <cppmetrics/cppmetrics.h>

int main() {
    cppmetrics::core::MetricRegistryPtr registry(
        cppmetrics::core::MetricRegistry::DEFAULT_REGISTRY());

    // More initialization.

    cppmetrics::core::CounterPtr query_counter(registry->counter("get_requests"));
    query_counter->increment();
    // More  processing
    {
       cppmetrics::core::TimerContextPtr timer(
            registry->timer("query_process")->timerContextPtr());
       // Do some computation or IO.
       // timer stats will be updated in the registry at the end of the scope.                
    }
    return 0;
}
