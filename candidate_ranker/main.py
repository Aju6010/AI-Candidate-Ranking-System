"""Main entry point for the candidate ranking system."""
import sys
import argparse
from pathlib import Path
from typing import Optional

from src.config import settings
from src.data_processor import DataProcessor
from src.engines import HybridRankingEngine


def main(
    job_file: str,
    candidates_file: str,
    output_format: str = "csv",
    top_n: Optional[int] = None,
    output_file: Optional[str] = None,
):
    """Main function to rank candidates from files.
    
    Args:
        job_file: Path to job description JSON file
        candidates_file: Path to candidates JSON file
        output_format: Output format ('csv' or 'json')
        top_n: Number of top candidates to return
        output_file: Path to save results (optional)
    """
    try:
        print("🚀 AI Candidate Ranking System")
        print("=" * 50)
        
        # Normalize file path to use current project data if needed
        candidate_path = Path(job_file)
        if not candidate_path.exists():
            fallback = Path(__file__).resolve().parent / "data" / "sample_dataset.json"
            if fallback.exists():
                job_file = str(fallback)
                candidates_file = str(fallback)

        # Load data
        print(f"\n📄 Loading job description from: {job_file}")
        job_description = DataProcessor.load_job_description_from_json(job_file)
        print(f"✓ Job loaded: {job_description.title} at {job_description.company}")
        
        print(f"\n👥 Loading candidates from: {candidates_file}")
        candidates = DataProcessor.load_candidates_from_json(candidates_file)
        print(f"✓ Loaded {len(candidates)} candidates")
        
        if not candidates:
            print("❌ No candidates found!")
            return
        
        # Prepare ranking
        top_n = top_n or settings.MAX_CANDIDATES_RETURNED
        print(f"\n🎯 Ranking candidates (top {top_n})...")
        
        # Initialize ranking engine
        ranking_engine = HybridRankingEngine()
        
        # Perform ranking
        ranked = ranking_engine.rank_candidates(
            job_description=job_description,
            candidates=candidates,
            top_n=top_n,
        )
        
        print(f"✓ Ranked {len(ranked)} candidates\n")
        
        # Display results
        print("📊 Top Rankings:")
        print("-" * 100)
        print(f"{'Rank':<5} {'Candidate':<25} {'Score':<8} {'Skills':<8} {'Exp':<8} {'Behavioral':<12} {'Recommendation':<20}")
        print("-" * 100)
        
        for result in ranked:
            print(
                f"{result.rank:<5} "
                f"{result.candidate_name:<25} "
                f"{result.overall_score:<8.2f} "
                f"{result.skill_match_score:<8.2f} "
                f"{result.experience_alignment:<8.2f} "
                f"{result.behavioral_signal_score:<12.2f} "
                f"{result.recommendation[:20]:<20}"
            )
        
        # Save results
        if output_file is None:
            output_file = settings.OUTPUT_PATH / f"rankings_{job_description.id}.{output_format}"
        
        print(f"\n💾 Saving results to: {output_file}")
        DataProcessor.export_rankings(ranked, str(output_file), format=output_format)
        print("✓ Results saved successfully!\n")
        
        # Print detailed info for top candidate
        if ranked:
            top = ranked[0]
            print("🏆 Top Candidate Details:")
            print("-" * 50)
            print(f"Name: {top.candidate_name}")
            print(f"Overall Score: {top.overall_score}/10")
            print(f"Skill Match: {top.skill_match_score}")
            print(f"Experience Alignment: {top.experience_alignment}")
            print(f"Semantic Similarity: {top.semantic_similarity}")
            print(f"Behavioral Score: {top.behavioral_signal_score}")
            print(f"\nStrengths:")
            for strength in top.strengths:
                print(f"  ✓ {strength}")
            if top.gaps:
                print(f"\nGaps:")
                for gap in top.gaps:
                    print(f"  ✗ {gap}")
            print(f"\nRecommendation: {top.recommendation}")
        
        print("\n✅ Process completed successfully!")
    
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="AI-powered candidate ranking system"
    )
    
    parser.add_argument(
        "--job",
        required=True,
        help="Path to job description JSON file",
    )
    parser.add_argument(
        "--candidates",
        required=True,
        help="Path to candidates JSON file",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (optional)",
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json"],
        default="csv",
        help="Output format (default: csv)",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=None,
        help="Number of top candidates to return",
    )
    
    args = parser.parse_args()
    
    main(
        job_file=args.job,
        candidates_file=args.candidates,
        output_format=args.format,
        top_n=args.top_n,
        output_file=args.output,
    )
