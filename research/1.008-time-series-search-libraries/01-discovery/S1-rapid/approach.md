# S1: Rapid Discovery - Time Series Search Libraries

## Research Question

What are the primary Python libraries for time series search, similarity analysis, and pattern discovery (DTW, shapelets, matrix profiles)?

## Scope

**In Scope:**
- Dynamic Time Warping (DTW) implementations
- Shapelet discovery algorithms
- Time series similarity search
- Time series classification libraries
- Pattern matching and subsequence search
- Matrix profile methods

**Out of Scope:**
- Time series forecasting libraries (covered in 1.073)
- Statistical time series modeling (ARIMA, etc.)
- Pure visualization tools
- Database-specific time series extensions

## Methodology

### Discovery Strategy
1. **Primary sources**: GitHub repositories, PyPI listings, academic paper implementations
2. **Key search terms**: "DTW python", "shapelet discovery", "time series classification", "matrix profile", "time series similarity"
3. **Quality filters**: Active maintenance (commits in last year), documentation quality, citation count for academic implementations

### Library Selection Criteria
- **Popularity**: GitHub stars >100, PyPI downloads, community size
- **Functionality**: Covers core time series search capabilities (DTW, shapelets, or matrix profiles)
- **Maturity**: Production-ready or research-grade with clear status
- **Documentation**: README + examples minimum

### Profile Structure
Each library profile covers:
- **Overview**: What it does, primary use cases
- **Core Features**: DTW variants, shapelet methods, search algorithms
- **Performance**: Speed characteristics, scalability notes
- **Ecosystem**: Dependencies, integration with scikit-learn/numpy/scipy
- **Community**: GitHub stats, maintenance status
- **Use Cases**: Typical applications
- **Sources**: Documentation, repository, papers

## Target Libraries (Initial List)

1. **tslearn** - Comprehensive ML for time series (DTW, shapelets, clustering)
2. **stumpy** - Matrix profile for pattern discovery
3. **sktime** - Scikit-learn style time series toolkit (includes classification)
4. **tsfresh** - Automatic feature extraction for classification
5. **seglearn** - Time series segmentation and classification
6. **pyts** - Time series transformations and classification
7. **dtaidistance** - Fast DTW distance calculations
8. **matrixprofile-ts** - Matrix profile implementation

## Expected Deliverables

- 8 library profiles (~300-500 lines each)
- `recommendations.md` with quick-reference comparison table
- Source documentation for each library (docs, repo, papers)

## Time Budget

**Target**: 3-4 hours
- Library discovery and filtering: 1 hour
- Profile creation (8 libraries): 2-2.5 hours
- Synthesis and recommendations: 0.5 hours
