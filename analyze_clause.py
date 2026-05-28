from app.retrieval.clause_analyzer import ClauseAnalyzer


def main():

    analyzer = ClauseAnalyzer(top_k=5)

    print("=" * 60)
    print("   LEGAL CLAUSE ANALYZER")
    print("   Powered by Legal Knowledge Base")
    print("=" * 60)

    while True:

        print("\nPaste your contract clause below.")
        print("(Type 'exit' to quit)\n")

        # collect multiline input until user enters blank line
        lines = []
        while True:
            line = input()
            if line.lower() == "exit":
                print("Goodbye.")
                return
            if line == "":
                break
            lines.append(line)

        clause = " ".join(lines).strip()

        if not clause:
            print("[ERROR] No clause entered. Try again.")
            continue

        print("\n" + "=" * 60)
        print("ANALYZING CLAUSE...")
        print("=" * 60)

        analysis = analyzer.analyze(clause)

        print("\n" + "=" * 60)
        print("ANALYSIS RESULT")
        print("=" * 60)
        print(analysis)
        print("\n" + "=" * 60)

        again = input("\nAnalyze another clause? (yes/no): ").strip().lower()
        if again != "yes":
            print("Goodbye.")
            break


if __name__ == "__main__":
    main()