from urllib.parse import urlparse, parse_qs
from utils import (generate_df,generate_combined_score,combined_score_aggregation,
                   generate_location,predict_categories, save_df_to_csv)

if __name__ == '__main__':
    # destination = 'Seoul'
    url = "https://www.google.com/travel/things-to-do/see-all?dest_mid=%2Fm%2F0hsqf&dest_state_type=sattd&dest_src=yts&q=seoul&ved=0CAMQ__kHahcKEwiA2uu24Ir-AhUAAAAAHQAAAAAQCA"

    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    destination = query_params.get('q', [''])[0]
    print(destination)

    df = generate_df(url)
    df = generate_combined_score(df)
    df = combined_score_aggregation(df)
    df = generate_location(df, destination)
    df = predict_categories(df, destination)
    save_df_to_csv(df, destination)