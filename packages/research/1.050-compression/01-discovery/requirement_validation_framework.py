#!/usr/bin/env python3
"""
S3: Need-Driven Discovery - Requirement Validation Framework
Validates compression library performance against specific requirements
"""

import time
import psutil
import os
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class PerformanceRequirement:
    """Defines a specific performance requirement for validation"""
    name: str
    target_value: float
    unit: str
    operator: str  # '<', '>', '==', '<=', '>='
    critical: bool = True


@dataclass
class ValidationResult:
    """Results of requirement validation testing"""
    requirement: PerformanceRequirement
    measured_value: float
    passed: bool
    deviation_percent: float
    notes: str = ""


class CompressionLibraryTester(ABC):
    """Abstract base for compression library testing"""

    @abstractmethod
    def compress(self, data: bytes) -> bytes:
        pass

    @abstractmethod
    def decompress(self, compressed_data: bytes) -> bytes:
        pass

    @abstractmethod
    def get_library_name(self) -> str:
        pass


class RequirementValidator:
    """
    S3 Need-Driven Discovery validation framework
    Tests actual performance against defined requirements
    """

    def __init__(self):
        self.requirements = self._define_requirements()
        self.test_data_sizes = [1024*1024, 10*1024*1024, 100*1024*1024]  # 1MB, 10MB, 100MB

    def _define_requirements(self) -> List[PerformanceRequirement]:
        """Define specific requirements based on business needs"""
        return [
            PerformanceRequirement(
                name="compression_speed_100mb",
                target_value=1.0,
                unit="seconds",
                operator="<",
                critical=True
            ),
            PerformanceRequirement(
                name="memory_usage_1gb",
                target_value=500.0,
                unit="MB",
                operator="<",
                critical=True
            ),
            PerformanceRequirement(
                name="compression_ratio",
                target_value=0.5,
                unit="ratio",
                operator="<",
                critical=True
            ),
            PerformanceRequirement(
                name="decompression_speed",
                target_value=0.5,
                unit="seconds",
                operator="<",
                critical=False
            ),
            PerformanceRequirement(
                name="cpu_efficiency",
                target_value=80.0,
                unit="percent",
                operator="<",
                critical=False
            )
        ]

    def generate_test_data(self, size: int) -> bytes:
        """Generate test data for compression testing"""
        # Mix of compressible and incompressible data for realistic testing
        compressible = b"A" * (size // 2)
        incompressible = os.urandom(size // 2)
        return compressible + incompressible

    def measure_compression_performance(self,
                                      tester: CompressionLibraryTester,
                                      data_size: int) -> Dict[str, float]:
        """Measure compression performance metrics"""
        test_data = self.generate_test_data(data_size)

        # Memory monitoring
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Compression timing
        start_time = time.time()
        cpu_start = psutil.cpu_percent()

        compressed_data = tester.compress(test_data)

        compression_time = time.time() - start_time
        peak_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_used = peak_memory - initial_memory

        # Decompression timing
        decomp_start = time.time()
        decompressed_data = tester.decompress(compressed_data)
        decompression_time = time.time() - decomp_start

        cpu_end = psutil.cpu_percent()
        cpu_usage = max(cpu_end - cpu_start, 0)

        # Validate data integrity
        data_integrity = test_data == decompressed_data

        # Calculate compression ratio
        compression_ratio = len(compressed_data) / len(test_data)

        return {
            "compression_time": compression_time,
            "decompression_time": decompression_time,
            "memory_used": memory_used,
            "compression_ratio": compression_ratio,
            "cpu_usage": cpu_usage,
            "data_integrity": data_integrity,
            "original_size": len(test_data),
            "compressed_size": len(compressed_data)
        }

    def validate_requirements(self,
                            tester: CompressionLibraryTester) -> List[ValidationResult]:
        """Validate library performance against all requirements"""
        results = []

        # Test with 100MB data for speed requirements
        perf_100mb = self.measure_compression_performance(tester, 100*1024*1024)

        # Validate compression speed requirement
        speed_req = next(r for r in self.requirements if r.name == "compression_speed_100mb")
        speed_result = self._validate_single_requirement(
            speed_req,
            perf_100mb["compression_time"]
        )
        results.append(speed_result)

        # Validate compression ratio requirement
        ratio_req = next(r for r in self.requirements if r.name == "compression_ratio")
        ratio_result = self._validate_single_requirement(
            ratio_req,
            perf_100mb["compression_ratio"]
        )
        results.append(ratio_result)

        # Validate decompression speed
        decomp_req = next(r for r in self.requirements if r.name == "decompression_speed")
        decomp_result = self._validate_single_requirement(
            decomp_req,
            perf_100mb["decompression_time"]
        )
        results.append(decomp_result)

        # Validate memory usage (use smaller test for memory requirement)
        memory_req = next(r for r in self.requirements if r.name == "memory_usage_1gb")
        # Scale down test for practical validation
        perf_10mb = self.measure_compression_performance(tester, 10*1024*1024)
        estimated_1gb_memory = perf_10mb["memory_used"] * 100  # Rough scaling
        memory_result = self._validate_single_requirement(
            memory_req,
            estimated_1gb_memory
        )
        memory_result.notes = "Estimated from 10MB test scaled to 1GB"
        results.append(memory_result)

        # Validate CPU efficiency
        cpu_req = next(r for r in self.requirements if r.name == "cpu_efficiency")
        cpu_result = self._validate_single_requirement(
            cpu_req,
            perf_100mb["cpu_usage"]
        )
        results.append(cpu_result)

        return results

    def _validate_single_requirement(self,
                                   requirement: PerformanceRequirement,
                                   measured_value: float) -> ValidationResult:
        """Validate a single requirement against measured value"""

        # Determine if requirement is met
        if requirement.operator == "<":
            passed = measured_value < requirement.target_value
        elif requirement.operator == ">":
            passed = measured_value > requirement.target_value
        elif requirement.operator == "<=":
            passed = measured_value <= requirement.target_value
        elif requirement.operator == ">=":
            passed = measured_value >= requirement.target_value
        elif requirement.operator == "==":
            passed = abs(measured_value - requirement.target_value) < 0.01
        else:
            passed = False

        # Calculate deviation percentage
        if requirement.target_value != 0:
            deviation = ((measured_value - requirement.target_value) /
                        requirement.target_value) * 100
        else:
            deviation = 0.0

        return ValidationResult(
            requirement=requirement,
            measured_value=measured_value,
            passed=passed,
            deviation_percent=deviation
        )

    def generate_requirement_satisfaction_score(self,
                                              results: List[ValidationResult]) -> float:
        """Calculate overall requirement satisfaction score"""
        total_weight = 0
        weighted_score = 0

        for result in results:
            weight = 3 if result.requirement.critical else 1
            score = 100 if result.passed else max(0, 100 - abs(result.deviation_percent))

            weighted_score += score * weight
            total_weight += weight

        return weighted_score / total_weight if total_weight > 0 else 0

    def print_validation_report(self,
                              tester: CompressionLibraryTester,
                              results: List[ValidationResult]):
        """Print detailed validation report"""
        print(f"\n=== S3 Need-Driven Discovery Validation Report ===")
        print(f"Library: {tester.get_library_name()}")
        print(f"Methodology: Requirement-based performance validation")
        print("-" * 60)

        for result in results:
            status = "✓ PASS" if result.passed else "✗ FAIL"
            critical = "(CRITICAL)" if result.requirement.critical else "(optional)"

            print(f"{status} {result.requirement.name} {critical}")
            print(f"    Target: {result.requirement.operator} {result.requirement.target_value} {result.requirement.unit}")
            print(f"    Measured: {result.measured_value:.3f} {result.requirement.unit}")
            print(f"    Deviation: {result.deviation_percent:+.1f}%")
            if result.notes:
                print(f"    Notes: {result.notes}")
            print()

        score = self.generate_requirement_satisfaction_score(results)
        print(f"Overall Requirement Satisfaction Score: {score:.1f}%")
        print(f"Need-Driven Discovery Recommendation: {'ACCEPT' if score >= 80 else 'REJECT'}")


# Example implementation for demonstration
class ZstandardTester(CompressionLibraryTester):
    """Example implementation for zstandard library testing"""

    def __init__(self):
        try:
            import zstandard as zstd
            self.compressor = zstd.ZstdCompressor(level=3)
            self.decompressor = zstd.ZstdDecompressor()
        except ImportError:
            raise ImportError("zstandard library not available for testing")

    def compress(self, data: bytes) -> bytes:
        return self.compressor.compress(data)

    def decompress(self, compressed_data: bytes) -> bytes:
        return self.decompressor.decompress(compressed_data)

    def get_library_name(self) -> str:
        return "python-zstandard"


def main():
    """
    S3 Need-Driven Discovery validation example
    Demonstrates requirement-based library evaluation
    """
    print("S3 Need-Driven Discovery: Compression Library Validation")
    print("Methodology: Define requirements, test solutions, validate fit")

    validator = RequirementValidator()

    print("\nDefined Requirements:")
    for req in validator.requirements:
        critical = "(CRITICAL)" if req.critical else "(optional)"
        print(f"  {req.name}: {req.operator} {req.target_value} {req.unit} {critical}")

    # Note: Actual testing would require library installation
    print("\nValidation framework ready for library testing")
    print("Install target libraries and run validation tests")
    print("Example: python requirement_validation_framework.py")


if __name__ == "__main__":
    main()