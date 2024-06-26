from google.cloud import aiplatform
from google.cloud.aiplatform import MatchingEngineIndex, MatchingEngineIndexEndpoint

def initialize_vertex_ai(project_id, region, bucket_name):
    aiplatform.init(project=project_id, location=region, staging_bucket=bucket_name)

def create_index(index_name, dimensions = 768, approximate_neighbors_count=150):
    index = MatchingEngineIndex.create_tree_ah_index(
    display_name=index_name,
    dimensions=dimensions, 
    approximate_neighbors_count=approximate_neighbors_count,
    distance_measure_type="COSINE_DISTANCE")

    return index

def get_index(index_id:str):
    my_index = aiplatform.MatchingEngineIndex(index_id)
    return my_index

def get_index_endpoint(index_endpoint_id:str):
    my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint("1234567890123456789")
    return my_index_endpoint

def deploy_index(index_name, endpoint_name):
    index_endpoint = MatchingEngineIndexEndpoint.create(
    display_name=endpoint_name,
    public_endpoint_enabled=True)

    return index_endpoint

def add_documents_to_index(index_name, documents):
    pass

