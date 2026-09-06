"""
Example usage of Iterative Delta Debugging Minimizer Skill.
"""

from client import DeltaDebuggingMinimizer


def main():
    print("=== Iterative Delta Debugging (ddmin) Minimizer Demonstration ===")
    minimizer = DeltaDebuggingMinimizer()

    # Large failing input list (e.g. SQL query tokens or config directives)
    # The failure occurs specifically when 'SELECT' and 'DROP' co-exist.
    failing_input = [
        "SET", "TIMEOUT", "=", "30", ";",
        "SELECT", "*", "FROM", "users", "WHERE", "active", "=", "1", ";",
        "DROP", "TABLE", "temp_logs", ";",
        "COMMIT", ";"
    ]

    def test_reproduces_bug(tokens):
        # Bug triggers only if BOTH "SELECT" and "DROP" are present
        return "SELECT" in tokens and "DROP" in tokens

    print(f"Original Input ({len(failing_input)} tokens):")
    print(" ", failing_input)

    res = minimizer.minimize(failing_input, test_reproduces_bug)

    print("\nMinimal Reproducible Example (MRE):")
    print("  Tokens:    ", res["minimal_elements"])
    print("  Size:      ", res["minimized_size"], "tokens")
    print("  Reduction: ", res["reduction_percentage"])
    print("  Steps:     ", res["steps"])


if __name__ == "__main__":
    main()
