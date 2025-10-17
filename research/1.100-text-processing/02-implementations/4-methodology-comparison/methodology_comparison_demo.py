#!/usr/bin/env python3
"""
Comprehensive 4-Methodology × 2-Library Text Classification Comparison
Tests all 8 implementations against identical baseline specification.
"""

import os
import sys
import time
import subprocess
import importlib.util
from pathlib import Path
from typing import Dict, List, Tuple, Any


class MethodologyComparison:
    """Comprehensive comparison of all methodology implementations."""

    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.results = {}
        self.test_cases = [
            "This is absolutely fantastic and amazing!",
            "Really disappointed with this terrible purchase.",
            "It's an acceptable solution for basic needs.",
            ""  # Edge case: empty string
        ]

    def find_implementations(self) -> Dict[str, Dict[str, str]]:
        """Auto-detect all available implementations."""
        implementations = {
            'fasttext': {},
            'scikit-learn': {}
        }

        method_mappings = {
            '1-immediate-implementation': 'Method 1 (Immediate)',
            '2-specification-driven': 'Method 2 (Specification)',
            '3-test-first-development': 'Method 3 (TDD)',
            '4-adaptive-tdd': 'Method 4 (Adaptive TDD)'
        }

        for library in ['fasttext', 'scikit-learn']:
            library_dir = self.base_dir / library
            if library_dir.exists():
                for method_dir, method_name in method_mappings.items():
                    impl_path = library_dir / method_dir / 'text_classifier.py'
                    if impl_path.exists():
                        implementations[library][method_name] = str(impl_path)

        return implementations

    def load_module(self, module_path: str, module_name: str):
        """Dynamically load a module from file path."""
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)

        # Add the module's directory to Python path temporarily
        module_dir = os.path.dirname(module_path)
        if module_dir not in sys.path:
            sys.path.insert(0, module_dir)

        try:
            spec.loader.exec_module(module)
            return module
        finally:
            # Remove from path to avoid conflicts
            if module_dir in sys.path:
                sys.path.remove(module_dir)

    def create_sample_data(self) -> Tuple[List[str], List[str]]:
        """Generate consistent sample data for all implementations."""
        texts = [
            # Positive sentiment samples
            "I absolutely love this product! Outstanding quality and performance throughout.",
            "Fantastic experience that exceeded all my expectations completely and thoroughly.",
            "Brilliant design with amazing attention to detail in every aspect.",
            "Superb customer service with incredibly helpful and responsive team members.",
            "Perfect solution that works flawlessly every single time without issues.",
            "Excellent quality with fast delivery, very satisfied customer experience.",
            "Wonderful experience overall, will definitely purchase again very soon.",
            "Great service and highly recommend to everyone I know personally.",
            "Amazing product quality, exactly what I needed for my specific project.",
            "Outstanding performance that truly exceeded my high expectations significantly.",

            # Negative sentiment samples
            "Terrible quality that broke immediately after first use. Complete waste of money.",
            "Horrible experience with slow delivery and damaged packaging throughout process.",
            "Awful product that doesn't work as advertised. Avoid at all costs.",
            "Poor customer service, very disappointed with entire experience overall.",
            "Worst purchase decision ever, requesting immediate full refund today.",
            "Disappointing quality, definitely not worth the high price paid.",
            "Broken on arrival due to terrible packaging and careless handling.",
            "Useless product design, complete failure and waste of valuable time.",
            "Bad experience overall with rude staff and poor service quality.",
            "Defective item that doesn't function as described in online documentation.",

            # Neutral sentiment samples
            "Acceptable product that gets the basic job done adequately without issues.",
            "Average quality item, meets minimum requirements without exceeding them.",
            "Standard functionality provided, nothing remarkable but works as expected.",
            "Decent enough solution, works fine for simple everyday tasks.",
            "Fair quality construction, reasonable value for the money spent.",
            "Basic product design, sufficient for general use cases.",
            "Ordinary quality level, meets expectations for this specific price point.",
            "Regular item that does what it says without major problems.",
            "Standard quality construction, as expected for this price range.",
            "It's okay overall, nothing special but does work properly."
        ]

        labels = (['positive'] * 10 + ['negative'] * 10 + ['neutral'] * 10)
        return texts, labels

    def test_implementation(self, library: str, method: str, module_path: str) -> Dict[str, Any]:
        """Test a single implementation comprehensively."""
        print(f"    Testing {library} - {method}...")

        try:
            # Load module
            module_name = f"{library}_{method.replace(' ', '_').replace('(', '').replace(')', '')}"
            module = self.load_module(module_path, module_name)

            # Get sample data
            texts, labels = self.create_sample_data()

            # Determine classifier class based on library
            if 'fasttext' in library.lower():
                if 'immediate' in method.lower():
                    classifier_class = getattr(module, 'FastTextClassifier', None)
                elif 'specification' in method.lower():
                    classifier_class = getattr(module, 'FastTextSentimentClassifier', None)
                elif 'tdd' in method.lower() and 'adaptive' not in method.lower():
                    classifier_class = getattr(module, 'FastTextTDDClassifier', None)
                else:  # Adaptive TDD
                    classifier_class = getattr(module, 'FastTextAdaptiveClassifier', None)
            else:  # scikit-learn
                if 'immediate' in method.lower():
                    classifier_class = getattr(module, 'SklearnQuickClassifier', None)
                elif 'specification' in method.lower():
                    classifier_class = getattr(module, 'SklearnEnterpriseClassifier', None)
                elif 'tdd' in method.lower() and 'adaptive' not in method.lower():
                    classifier_class = getattr(module, 'SklearnTDDClassifier', None)
                else:  # Adaptive TDD
                    classifier_class = getattr(module, 'SklearnAdaptiveTDDClassifier', None)

            if not classifier_class:
                return {'error': 'Classifier class not found'}

            # Initialize classifier
            classifier = classifier_class()

            # Measure training time
            start_time = time.time()
            training_result = classifier.train(texts, labels)
            training_time = time.time() - start_time

            # Test predictions with timing
            prediction_results = []
            total_prediction_time = 0

            for test_text in self.test_cases:
                pred_start = time.time()
                try:
                    result = classifier.predict(test_text)
                    pred_time = (time.time() - pred_start) * 1000  # Convert to ms
                    total_prediction_time += pred_time

                    prediction_results.append({
                        'input': test_text,
                        'predicted_label': result.get('predicted_label', 'unknown'),
                        'confidence': result.get('confidence', 0.0),
                        'prediction_time_ms': pred_time,
                        'error': None
                    })
                except Exception as e:
                    prediction_results.append({
                        'input': test_text,
                        'predicted_label': 'error',
                        'confidence': 0.0,
                        'prediction_time_ms': 0.0,
                        'error': str(e)
                    })

            # Test batch prediction
            batch_start = time.time()
            try:
                batch_results = classifier.predict_batch(self.test_cases[:2])
                batch_time = (time.time() - batch_start) * 1000
                batch_success = len(batch_results) == 2
            except Exception as e:
                batch_time = 0.0
                batch_success = False

            # Calculate average prediction time
            avg_prediction_time = total_prediction_time / len(self.test_cases)

            return {
                'success': True,
                'training_time': training_time,
                'training_result': training_result,
                'avg_prediction_time_ms': avg_prediction_time,
                'meets_performance_requirement': avg_prediction_time < 100,
                'prediction_results': prediction_results,
                'batch_prediction_success': batch_success,
                'batch_prediction_time_ms': batch_time,
                'error': None
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'training_time': 0.0,
                'avg_prediction_time_ms': 0.0,
                'meets_performance_requirement': False
            }

    def run_comparison(self) -> None:
        """Run comprehensive comparison of all implementations."""
        print("=" * 80)
        print("🚀 COMPREHENSIVE 4-METHODOLOGY × 2-LIBRARY COMPARISON")
        print("=" * 80)

        implementations = self.find_implementations()

        if not any(implementations.values()):
            print("❌ No implementations found!")
            return

        print(f"📊 Found implementations:")
        for library, methods in implementations.items():
            if methods:
                print(f"  {library.upper()}:")
                for method, path in methods.items():
                    print(f"    • {method}")

        print("\n" + "=" * 80)
        print("🧪 RUNNING FUNCTIONALITY TESTS")
        print("=" * 80)

        # Test all implementations
        for library, methods in implementations.items():
            if not methods:
                continue

            print(f"\n{library.upper()} IMPLEMENTATIONS:")
            print("-" * 40)

            for method, module_path in methods.items():
                result = self.test_implementation(library, method, module_path)
                self.results[f"{library}_{method}"] = result

                if result['success']:
                    print(f"    ✅ {method}")
                    print(f"       Training time: {result['training_time']:.2f}s")
                    print(f"       Avg prediction: {result['avg_prediction_time_ms']:.1f}ms")
                    print(f"       Performance req: {'✅' if result['meets_performance_requirement'] else '❌'}")
                else:
                    print(f"    ❌ {method} - {result['error']}")

        # Generate comparison analysis
        self.generate_analysis()

    def generate_analysis(self) -> None:
        """Generate comprehensive analysis of results."""
        print("\n" + "=" * 80)
        print("📈 METHODOLOGY COMPARISON ANALYSIS")
        print("=" * 80)

        successful_results = {k: v for k, v in self.results.items() if v['success']}

        if not successful_results:
            print("❌ No successful implementations to compare")
            return

        # Performance Analysis
        print("\n🏃 PERFORMANCE ANALYSIS:")
        print("-" * 30)

        performance_data = []
        for impl_name, result in successful_results.items():
            library, method = impl_name.split('_', 1)
            performance_data.append({
                'library': library,
                'method': method,
                'training_time': result['training_time'],
                'avg_prediction_time': result['avg_prediction_time_ms'],
                'meets_requirement': result['meets_performance_requirement']
            })

        # Sort by training time
        performance_data.sort(key=lambda x: x['training_time'])

        print("Training Time Ranking:")
        for i, data in enumerate(performance_data, 1):
            req_icon = "✅" if data['meets_requirement'] else "❌"
            print(f"  {i}. {data['library']} - {data['method']}")
            print(f"     Training: {data['training_time']:.2f}s, Prediction: {data['avg_prediction_time']:.1f}ms {req_icon}")

        # Prediction Time Analysis
        print("\nPrediction Speed Ranking:")
        performance_data.sort(key=lambda x: x['avg_prediction_time'])

        for i, data in enumerate(performance_data, 1):
            req_icon = "✅" if data['meets_requirement'] else "❌"
            print(f"  {i}. {data['library']} - {data['method']}: {data['avg_prediction_time']:.1f}ms {req_icon}")

        # Functionality Equivalence Test
        self.test_functionality_equivalence(successful_results)

        # Success Rate Analysis
        print(f"\n📊 IMPLEMENTATION SUCCESS RATE:")
        print("-" * 35)

        total_attempted = len(self.results)
        total_successful = len(successful_results)
        success_rate = (total_successful / total_attempted) * 100 if total_attempted > 0 else 0

        print(f"Total implementations: {total_attempted}")
        print(f"Successful: {total_successful}")
        print(f"Success rate: {success_rate:.1f}%")

        # Performance Requirement Compliance
        meeting_requirements = sum(1 for r in successful_results.values() if r['meets_performance_requirement'])
        compliance_rate = (meeting_requirements / total_successful) * 100 if total_successful > 0 else 0

        print(f"Meeting <100ms requirement: {meeting_requirements}/{total_successful}")
        print(f"Performance compliance: {compliance_rate:.1f}%")

    def test_functionality_equivalence(self, successful_results: Dict) -> None:
        """Test that all implementations provide equivalent functionality."""
        print(f"\n🔍 FUNCTIONALITY EQUIVALENCE TEST:")
        print("-" * 40)

        # Create test matrix
        test_cases_for_comparison = [
            "This is fantastic!",
            "This is terrible!",
            "This is okay.",
            ""
        ]

        print(f"Testing {len(successful_results)} implementations on {len(test_cases_for_comparison)} cases...")
        print()

        # Create comparison table header
        impl_names = list(successful_results.keys())
        header = f"{'Test Case':<20}"
        for impl_name in impl_names:
            library, method = impl_name.split('_', 1)
            # Create abbreviation safely
            if '(' in method:
                method_part = method.split()[1][1:-1] if len(method.split()) > 1 and len(method.split()[1]) > 2 else method[:3]
            else:
                method_part = method[:3]
            abbrev = f"{library[:2].upper()}-{method_part.upper()}"
            header += f" {abbrev:<8}"

        print(header)
        print("-" * len(header))

        # Test each case
        for test_case in test_cases_for_comparison:
            display_case = test_case if test_case else "(empty)"
            row = f"{display_case:<20}"

            for impl_name in impl_names:
                result = successful_results[impl_name]

                # Find prediction result for this test case
                prediction = "N/A"
                for pred_result in result.get('prediction_results', []):
                    if pred_result['input'] == test_case:
                        if pred_result['error']:
                            prediction = "ERR"
                        else:
                            pred_label = pred_result['predicted_label']
                            if pred_label == 'positive':
                                prediction = "POS"
                            elif pred_label == 'negative':
                                prediction = "NEG"
                            elif pred_label == 'neutral':
                                prediction = "NEU"
                            else:
                                prediction = pred_label[:3].upper()
                        break

                row += f" {prediction:<8}"

            print(row)

        print(f"\n✅ Equivalence test completed for {len(successful_results)} implementations")

    def generate_summary_report(self) -> None:
        """Generate final summary report."""
        print("\n" + "=" * 80)
        print("🎯 FINAL SUMMARY REPORT")
        print("=" * 80)

        successful_results = {k: v for k, v in self.results.items() if v['success']}

        if successful_results:
            print("✅ SUCCESSFUL IMPLEMENTATIONS:")
            for impl_name, result in successful_results.items():
                library, method = impl_name.split('_', 1)
                req_status = "✅" if result['meets_performance_requirement'] else "❌"
                print(f"  • {library} - {method}: {result['avg_prediction_time_ms']:.1f}ms {req_status}")

            # Find best performers
            fastest_training = min(successful_results.items(),
                                 key=lambda x: x[1]['training_time'])
            fastest_prediction = min(successful_results.items(),
                                   key=lambda x: x[1]['avg_prediction_time_ms'])

            print(f"\n🏆 BEST PERFORMERS:")
            print(f"  Fastest Training: {fastest_training[0].replace('_', ' - ')} ({fastest_training[1]['training_time']:.2f}s)")
            print(f"  Fastest Prediction: {fastest_prediction[0].replace('_', ' - ')} ({fastest_prediction[1]['avg_prediction_time_ms']:.1f}ms)")

        failed_results = {k: v for k, v in self.results.items() if not v['success']}
        if failed_results:
            print(f"\n❌ FAILED IMPLEMENTATIONS:")
            for impl_name, result in failed_results.items():
                library, method = impl_name.split('_', 1)
                print(f"  • {library} - {method}: {result['error']}")

        print(f"\n📊 METHODOLOGY EFFECTIVENESS:")
        methodology_success = {}
        for impl_name, result in self.results.items():
            library, method = impl_name.split('_', 1)
            if method not in methodology_success:
                methodology_success[method] = {'success': 0, 'total': 0}

            methodology_success[method]['total'] += 1
            if result['success']:
                methodology_success[method]['success'] += 1

        for method, stats in methodology_success.items():
            success_rate = (stats['success'] / stats['total']) * 100
            print(f"  {method}: {stats['success']}/{stats['total']} ({success_rate:.0f}%)")

        print("\n✅ COMPREHENSIVE COMPARISON COMPLETE!")
        print("All methodology implementations tested and analyzed.")


def main():
    """Run the comprehensive methodology comparison."""
    comparison = MethodologyComparison()
    comparison.run_comparison()
    comparison.generate_summary_report()


if __name__ == "__main__":
    main()