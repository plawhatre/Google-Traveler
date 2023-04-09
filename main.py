from urllib.parse import urlparse, parse_qs
from utils import (generate_df,generate_combined_score,combined_score_aggregation,
                   generate_location,predict_categories, save_df_to_csv)

if __name__ == '__main__':
    urls = ["https://www.google.com/travel/things-to-do/see-all?dest_mid=%2Fm%2F03h64&dest_state_type=sattd&dest_src=yts&q=hong%20kong&ved=0CAEQ__kHahcKEwiIsJvdm5z-AhUAAAAAHQAAAAAQDQ",
            "https://www.google.com/travel/things-to-do/see-all?dest_mid=%2Fm%2F04thp&dest_state_type=sattd&dest_src=yts&q=macau&ved=0CAEQ__kHahcKEwiQ6P3N0Zz-AhUAAAAAHQAAAAAQBg",
            "https://www.google.com/travel/things-to-do/see-all?dest_mid=%2Fm%2F0hsqf&dest_state_type=sattd&dest_src=yts&q=seoul&ved=0CAMQ__kHahcKEwiA2uu24Ir-AhUAAAAAHQAAAAAQCA",
            "https://www.google.com/travel/things-to-do/see-all?dest_mid=%2Fm%2F02716j&dest_state_type=sattd&dest_src=yts&q=gyeongju&ved=0CAQQ__kHahgKEwiYkMT80Zz-AhUAAAAAHQAAAAAQlwE",
            "https://www.google.com/travel/things-to-do/places?dest_mid=%2Fm%2F0hv7l&dest_state_type=sap&dest_src=yts&q=busan&ved=0CAEQ__kHahcKEwjQyZPR0Zz-AhUAAAAAHQAAAAAQfA"]

    for url in urls:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        destination = query_params.get('q', [''])[0]
        print('*-*'*20 + destination.upper()+ '*-*'*20)

        df = generate_df(url)
        df = generate_combined_score(df)
        df = combined_score_aggregation(df)
        df = generate_location(df, destination)
        df = predict_categories(df, destination)
        save_df_to_csv(df, destination)