
import spoonacular
from spoonacular.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.spoonacular.com
# See configuration.py for a list of all supported configuration parameters.
configuration = spoonacular.Configuration(
    host = "https://api.spoonacular.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKeyScheme
configuration.api_key['apiKeyScheme'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKeyScheme'] = 'Bearer'


# Enter a context with an instance of the API client
with spoonacular.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = spoonacular.DefaultApi(api_client)
    analyze_recipe_request = {"title":"Spaghetti Carbonara","servings":2,"ingredients":["1 lb spaghetti","3.5 oz pancetta","2 Tbsps olive oil","1  egg","0.5 cup parmesan cheese"],"instructions":"Bring a large pot of water to a boil and season generously with salt. Add the pasta to the water once boiling and cook until al dente. Reserve 2 cups of cooking water and drain the pasta. "} # AnalyzeRecipeRequest | Example request body.
    language = 'en' # str | The input language, either \"en\" or \"de\". (optional)
    include_nutrition = false # bool | Whether nutrition data should be added to correctly parsed ingredients. (optional)
    include_taste = false # bool | Whether taste data should be added to correctly parsed ingredients. (optional)

    try:
        # Analyze Recipe
        api_response = api_instance.analyze_recipe(analyze_recipe_request, language=language, include_nutrition=include_nutrition, include_taste=include_taste)
        print("The response of DefaultApi->analyze_recipe:\n")
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->analyze_recipe: %s\n" % e)
