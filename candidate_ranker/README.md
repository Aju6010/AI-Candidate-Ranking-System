# AI Candidate Ranking System

An intelligent candidate ranking system that uses hybrid scoring to match candidates with job descriptions. Instead of simple keyword matching, this system understands the full context of both jobs and candidates.

## Features

### Hybrid Ranking Engine
- **Semantic Similarity** (25%): Uses Sentence Transformers to understand semantic meaning beyond keywords
- **Skill Matching** (30%): Intelligent skill matching with fuzzy matching and synonym recognition
- **Experience Alignment** (25%): Scores years of experience, career level progression, and role fit
- **Behavioral Signals** (20%): Evaluates engagement through certifications, projects, GitHub activity, and community participation

### Multi-Signal Analysis
- Career history and progression
- Skill gap identification
- Platform engagement metrics
- Educational background
- Project portfolio assessment

### Multiple Deployment Options
- **CLI Tool**: Command-line interface for batch processing
- **REST API**: FastAPI-based service for real-time ranking
- **Batch Processing**: Process large candidate pools efficiently

## Project Structure

```
candidate_ranker/
├── src/
│   ├── models/
│   │   ├── candidate.py          # Data models (Pydantic)
│   │   └── __init__.py
│   ├── engines/
│   │   ├── embeddings.py         # Semantic similarity engine
│   │   ├── skill_matcher.py      # Skill matching engine
│   │   ├── experience.py         # Experience alignment scoring
│   │   ├── behavioral.py         # Behavioral signal analysis
│   │   ├── hybrid_ranker.py      # Main ranking engine
│   │   └── __init__.py
│   ├── app.py                    # FastAPI application
│   ├── config.py                 # Configuration management
│   ├── data_processor.py         # Data loading/saving utilities
│   └── __init__.py
├── data/
│   ├── sample_job.json           # Example job description
│   └── sample_candidates.json    # Example candidates
├── output/                       # Rankings output directory
├── main.py                       # CLI entry point
├── requirements.txt              # Dependencies
├── .env.example                  # Environment variables template
└── README.md                     # This file
```

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd candidate_ranker
```

### 2. Create and activate virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup environment
```bash
cp .env.example .env
# Edit .env if needed for custom configuration
```

## Usage

### CLI Usage

Rank candidates from JSON files:

```bash
python main.py --job data/sample_job.json --candidates data/sample_candidates.json --top-n 10
```

**Options:**
- `--job`: Path to job description JSON file (required)
- `--candidates`: Path to candidates JSON file (required)
- `--top-n`: Number of top candidates to return (default: 10)
- `--output`: Output file path (optional)
- `--format`: Output format: 'csv' or 'json' (default: 'csv')

**Example with default CSV output:**
```bash
python main.py \
  --job data/sample_job.json \
  --candidates data/sample_candidates.json \
  --top-n 10 \
  --format csv
```

**Example with explicit output file:**
```bash
python main.py \
  --job data/sample_job.json \
  --candidates data/sample_candidates.json \
  --top-n 10 \
  --output candidate_ranker/output/results.csv \
  --format csv
```

### API Usage

#### 1. Start the server
```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Access API documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### 3. Rank candidates via API

**Using JSON request:**
```bash
curl -X POST http://localhost:8000/rank \
  -H "Content-Type: application/json" \
  -d @request.json
```

**Using file upload:**
```bash
curl -X POST http://localhost:8000/rank-from-files \
  -F "job_file=@data/sample_job.json" \
  -F "candidates_file=@data/sample_candidates.json" \
  -F "top_n=5"
```

#### 4. List and download results
```bash
# List all results
curl http://localhost:8000/outputs

# Download specific result
curl http://localhost:8000/outputs/rankings_job_001.json -o results.json
```

## Input Data Format

### Job Description JSON
```json
{
  "id": "job_001",
  "title": "Senior ML Engineer",
  "company": "Tech Company",
  "description": "Full job description...",
  "required_skills": ["Python", "Machine Learning", "TensorFlow"],
  "required_experience_years": 5,
  "required_qualifications": ["B.S. in CS"],
  "preferred_skills": ["PyTorch", "Kubernetes"],
  "role_level": "Senior",
  "employment_type": "Full-time"
}
```

### Candidates JSON
```json
{
  "candidates": [
    {
      "id": "cand_001",
      "name": "John Doe",
      "email": "john@example.com",
      "current_role": "Senior Software Engineer",
      "current_company": "Previous Corp",
      "years_of_experience": 7,
      "skills": ["Python", "Machine Learning", "Docker"],
      "core_competencies": ["Backend", "ML"],
      "education": ["B.S. Computer Science"],
      "certifications": ["AWS Certified"],
      "projects": ["Recommendation system"],
      "platform_activity": {
        "github_contributions": 1500,
        "blog_posts": 5,
        "open_source_projects": 2
      }
    }
  ]
}
```

## Output Format

### Ranking Result CSV
```
rank,candidate_id,candidate_name,overall_score,semantic_similarity,skill_match_score,experience_alignment,behavioral_signal_score,matching_skills,missing_skills,strengths,gaps,recommendation
1,cand_001,Alice Johnson,9.2,0.95,0.9,0.88,0.85,"[Python, ML]","[]","[Excellent skills]","[]","STRONG MATCH"
```

### Ranking Result JSON
```json
{
  "job_id": "job_001",
  "ranked_candidates": [
    {
      "candidate_id": "cand_001",
      "candidate_name": "Alice Johnson",
      "overall_score": 9.2,
      "semantic_similarity": 0.95,
      "skill_match_score": 0.9,
      "experience_alignment": 0.88,
      "behavioral_signal_score": 0.85,
      "matching_skills": ["Python", "ML"],
      "missing_skills": [],
      "strengths": ["Excellent skill match"],
      "gaps": [],
      "recommendation": "STRONG MATCH - Highly recommended"
    }
  ]
}
```

### Notes
- If you run with `--format json` and no `--output`, the file is saved as `rankings_<job_id>.json`.
- If you run with `--format csv` and no `--output`, the file is saved as `rankings_<job_id>.csv`.

## Scoring Methodology

### Overall Score (0-10 scale)
The system calculates a weighted composite score:

```
Overall Score = (Semantic × 0.25) + (Skill Match × 0.30) + (Experience × 0.25) + (Behavioral × 0.20)
```

### Component Scores

**1. Semantic Similarity (25%)**
- Uses pre-trained Sentence Transformer models
- Compares embeddings of job description and candidate profile
- Range: 0-1 (normalized to 0-10)

**2. Skill Matching (30%)**
- Matches required skills (70% weight) and preferred skills (30% weight)
- Uses fuzzy matching with synonym recognition
- Identifies specific missing skills
- Range: 0-1

**3. Experience Alignment (25%)**
- Years of experience vs. requirements (40%)
- Role level progression (40%)
- Career trajectory and stability (20%)
- Range: 0-1

**4. Behavioral Signals (20%)**
- Platform activity (GitHub, blogs, open source)
- Certifications and continuous learning
- Personal projects and engagement
- Community participation
- Range: 0-1

### Recommendation Levels
- **STRONG MATCH (8.0+)**: Highly recommended for interview
- **GOOD MATCH (7.0-7.9)**: Consider for interview
- **MODERATE MATCH (6.0-6.9)**: May be worth considering
- **WEAK MATCH (<6.0)**: Limited fit

## Configuration

Edit `.env` file to customize:

```env
ENV=development
DEBUG=True
API_HOST=0.0.0.0
API_PORT=8000
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_MODEL=gpt2
MAX_CANDIDATES_RETURNED=10
DATA_PATH=./data
OUTPUT_PATH=./output
```

## Technologies Used

- **Python 3.9+**
- **FastAPI**: Web framework for APIs
- **Sentence Transformers**: Semantic embeddings
- **scikit-learn**: Machine learning utilities
- **Pydantic**: Data validation
- **Pandas**: Data processing
- **Transformers**: NLP models

## Performance

- Single candidate ranking: ~100-500ms
- Batch processing (1000 candidates): ~5-30 seconds
- API throughput: 10+ rankings/second
- Memory efficient: <2GB for 10k candidates

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0"]
```

Build and run:
```bash
docker build -t candidate-ranker .
docker run -p 8000:8000 candidate-ranker
```

### Production Server

Use with production ASGI server:

```bash
gunicorn src.app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Submit a pull request

## License

MIT License

## Support

For issues or questions, please open an issue on GitHub.

## Future Enhancements

- [ ] Fine-tuned models for specific industries
- [ ] Real-time resume parsing
- [ ] Integration with job boards (LinkedIn, Indeed, etc.)
- [ ] Advanced NLP for domain-specific terminology
- [ ] Custom weight configuration per job type
- [ ] Batch processing API endpoints
- [ ] Web UI for results visualization
- [ ] Feedback mechanism for model improvement
- [ ] Multi-language support

---

