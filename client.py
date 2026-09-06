"""
Iterative Delta Debugging Minimizer Skill Client
Pure Python Standard Library implementation of Delta Debugging (ddmin) (Zeller et al.).
Minimizes failing test inputs, large payloads, or lines of code into the minimal subset that still reproduces the failure.
"""

from typing import List, Callable, Any, Dict


class DeltaDebuggingMinimizer:
    """
    Implements the classical ddmin algorithm:
    Given a test function that returns FAIL on the full set,
    find a 1-minimal subset of elements that still triggers FAIL.
    """

    def minimize(self, elements: List[Any], test_func: Callable[[List[Any]], bool]) -> Dict[str, Any]:
        """
        :param elements: List of items (e.g. lines of code, characters, tokens).
        :param test_func: Callable returning True if failure reproduces, False otherwise.
        :return: Dict with minimal elements, steps taken, and reduction percentage.
        """
        if not elements:
            return {"minimal_elements": [], "steps": 0, "reduction": 1.0}

        # Verify initial full set reproduces failure
        if not test_func(elements):
            raise ValueError("Input elements do not trigger test failure initially")

        n = 2
        current = list(elements)
        steps = 0

        while len(current) >= 2:
            subsets = []
            k = len(current)
            chunk_size = (k + n - 1) // n

            for i in range(0, k, chunk_size):
                subsets.append(current[i:i + chunk_size])

            reduced = False

            # Test each subset (is failure inside subset?)
            for s in subsets:
                steps += 1
                if test_func(s):
                    current = s
                    n = max(n - 1, 2)
                    reduced = True
                    break

            if not reduced:
                # Test complement of each subset (is failure outside subset?)
                for s in subsets:
                    complement = [x for x in current if x not in s]
                    steps += 1
                    if complement and test_func(complement):
                        current = complement
                        n = max(n - 1, 2)
                        reduced = True
                        break

            if not reduced:
                if n >= len(current):
                    break
                n = min(n * 2, len(current))

        initial_len = len(elements)
        final_len = len(current)
        reduction = (initial_len - final_len) / initial_len if initial_len > 0 else 0.0

        return {
            "minimal_elements": current,
            "initial_size": initial_len,
            "minimized_size": final_len,
            "steps": steps,
            "reduction_percentage": f"{reduction * 100:.1f}%"
        }
