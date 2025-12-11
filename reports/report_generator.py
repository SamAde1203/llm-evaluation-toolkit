import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import numpy as np

class ReportGenerator:
    """Generate comprehensive evaluation reports."""
    
    def __init__(self, results: Dict[str, Any]):
        self.results = results
        self.df = self._create_dataframe()
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
    
    def _create_dataframe(self) -> pd.DataFrame:
        """Convert results to pandas DataFrame."""
        rows = []
        for sample in self.results['per_sample']:
            row = {
                'sample_id': sample['sample_id'],
                'prediction': sample['prediction'],
                'reference': sample['reference'],
            }
            # Add all scores
            for metric, score in sample['scores'].items():
                row[metric] = score
            rows.append(row)
        
        return pd.DataFrame(rows)
    
    def generate_markdown_report(self, output_path: str = None) -> str:
        """Generate a comprehensive markdown report."""
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"reports/evaluation_report_{timestamp}.md"
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generate visualizations
        viz_path = output_path.parent / "visualizations"
        viz_path.mkdir(exist_ok=True)
        
        # Create visualizations
        self._create_score_distribution_plot(viz_path / "score_distribution.png")
        self._create_correlation_heatmap(viz_path / "correlation_heatmap.png")
        self._create_metric_comparison_plot(viz_path / "metric_comparison.png")
        
        # Generate markdown
        md_content = self._build_markdown_content(viz_path)
        
        # Save report with UTF-8 encoding
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
        except UnicodeEncodeError:
            # Fallback: ASCII with replacements
            with open(output_path, 'w', encoding='ascii', errors='replace') as f:
                f.write(md_content)
        
        print(f"Report generated: {output_path}")
        return md_content
    
    def _create_score_distribution_plot(self, save_path: Path):
        """Create histogram of overall scores."""
        plt.figure(figsize=(10, 6))
        
        # Plot overall scores
        plt.hist(self.df['overall_score'], bins=20, alpha=0.7, edgecolor='black')
        plt.axvline(self.df['overall_score'].mean(), color='red', linestyle='--', 
                   label=f'Mean: {self.df["overall_score"].mean():.3f}')
        
        plt.xlabel('Overall Score', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.title('Distribution of Overall Evaluation Scores', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
    
    def _create_correlation_heatmap(self, save_path: Path):
        """Create correlation matrix of different metrics."""
        # Get only numeric score columns
        score_columns = [col for col in self.df.columns if col not in 
                        ['sample_id', 'prediction', 'reference']]
        
        if len(score_columns) < 2:
            return
        
        correlation_matrix = self.df[score_columns].corr()
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', 
                   center=0, square=True, linewidths=1, fmt='.2f')
        
        plt.title('Correlation Between Evaluation Metrics', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
    
    def _create_metric_comparison_plot(self, save_path: Path):
        """Create box plot comparing different metrics."""
        # Get only numeric score columns (excluding overall)
        score_columns = [col for col in self.df.columns if col not in 
                        ['sample_id', 'prediction', 'reference', 'overall_score']]
        
        if not score_columns:
            return
        
        # Melt dataframe for seaborn
        melted_df = pd.melt(self.df[score_columns], var_name='Metric', value_name='Score')
        
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=melted_df, x='Metric', y='Score')
        sns.stripplot(data=melted_df, x='Metric', y='Score', 
                     color='black', alpha=0.5, size=4)
        
        plt.xlabel('Evaluation Metric', fontsize=12)
        plt.ylabel('Score', fontsize=12)
        plt.title('Comparison of Different Evaluation Metrics', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
    
    def _build_markdown_content(self, viz_path: Path) -> str:
        """Build the complete markdown report."""
        lines = []
        
        # Header
        lines.append("# LLM Evaluation Report")
        lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Total Samples**: {self.results['metadata']['total_samples']}")
        lines.append("")
        
        # Summary Statistics
        lines.append("## Summary Statistics")
        lines.append("")
        
        # Aggregate scores table
        lines.append("### Aggregate Scores")
        lines.append("| Metric | Mean | Std Dev | Min | Max |")
        lines.append("|--------|------|---------|-----|-----|")
        
        for key, value in self.results['aggregate'].items():
            if key.endswith('_mean'):
                metric_name = key.replace('_mean', '')
                mean_val = value
                std_val = self.results['aggregate'].get(f'{metric_name}_std', 0)
                min_val = self.results['aggregate'].get(f'{metric_name}_min', 0)
                max_val = self.results['aggregate'].get(f'{metric_name}_max', 0)
                
                lines.append(f"| {metric_name} | {mean_val:.3f} | {std_val:.3f} | {min_val:.3f} | {max_val:.3f} |")
        
        lines.append("")
        
        # Visualizations
        lines.append("## Visualizations")
        lines.append("")
        lines.append("### Score Distribution")
        lines.append(f"![Score Distribution]({viz_path.name}/score_distribution.png)")
        lines.append("")
        
        lines.append("### Metric Correlation")
        lines.append(f"![Metric Correlation]({viz_path.name}/correlation_heatmap.png)")
        lines.append("")
        
        lines.append("### Metric Comparison")
        lines.append(f"![Metric Comparison]({viz_path.name}/metric_comparison.png)")
        lines.append("")
        
        # Top and Bottom Performers
        lines.append("## Sample Analysis")
        lines.append("")
        
        # Top 3
        top_samples = self.df.nlargest(3, 'overall_score')
        lines.append("### Top 3 Performers")
        for _, row in top_samples.iterrows():
            lines.append(f"**{row['sample_id']}** (Score: {row['overall_score']:.3f})")
            lines.append(f"- Prediction: {row['prediction']}")
            lines.append(f"- Reference: {row['reference']}")
            lines.append("")
        
        # Bottom 3
        bottom_samples = self.df.nsmallest(3, 'overall_score')
        lines.append("### Bottom 3 Performers")
        for _, row in bottom_samples.iterrows():
            lines.append(f"**{row['sample_id']}** (Score: {row['overall_score']:.3f})")
            lines.append(f"- Prediction: {row['prediction']}")
            lines.append(f"- Reference: {row['reference']}")
            lines.append("")
        
        # Recommendations
        lines.append("## Recommendations")
        lines.append("")
        lines.append("1. **Consider metric weights**: Adjust weights based on your use case.")
        lines.append("2. **Add custom metrics**: Implement domain-specific evaluation criteria.")
        lines.append("3. **Increase dataset size**: More samples provide more reliable statistics.")
        lines.append("4. **Benchmark against baselines**: Compare with other LLMs or human evaluations.")
        
        return "\n".join(lines)