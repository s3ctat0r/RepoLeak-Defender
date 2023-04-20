print("""

######                       #                               ######                                                   
#     # ###### #####   ####  #       ######   ##   #    #    #     # ###### ###### ###### #    # #####  ###### #####  
#     # #      #    # #    # #       #       #  #  #   #     #     # #      #      #      ##   # #    # #      #    # 
######  #####  #    # #    # #       #####  #    # ####      #     # #####  #####  #####  # #  # #    # #####  #    # 
#   #   #      #####  #    # #       #      ###### #  #      #     # #      #      #      #  # # #    # #      #####  
#    #  #      #      #    # #       #      #    # #   #     #     # #      #      #      #   ## #    # #      #   #  
#     # ###### #       ####  ####### ###### #    # #    #    ######  ###### #      ###### #    # #####  ###### #    # 
                                                                                                                      
""")

# author@Suprit
#Robin round for tokens
n = -1

def token_round_robin():
    global n
    n = n+1
    if n == len(tokens_list):
        n = 0
        current_token = tokens_list[n]
        return current_token 

#API search Function
def api_search(url):
    if args.dorks: 
        if args.keyword:
            sys.stdout.write(colored(
                '\r[+] Dorking with Keyword In Progress %d/%d\r' % (stats_dict['n_current'], stats_dict['n_total_urls']),
                "green"))
            sys.stdout.flush()
        else:
            sys.stdout.write(
                colored('\r[+] Dorking In Progress %d/%d\r' % (stats_dict['n_current'], stats_dict['n_total_urls']), "green"))
            sys.stdout.flush()

    elif args.keyword and not args.dorks:
        sys.stdout.write(
            colored('\r[+]  Keyword Search In Progress %d/%d\r' % (stats_dict['n_current'], stats_dict['n_total_urls']),
                    "green"))
        sys.stdout.flush()
stats_dict['n_current'] = stats_dict['n_current'] + 1
headers = {"Authorization": "token" + token_round_robin()}

try:
    r = requests.get(url, headers=headers)
    json = r.json()
    if args.limitbypass:
        if stats_dict['n_current'] % requests_per_minute == 0:
            for remaining in range(63, 0, -1):
                sys.stdout.write("\r")
                sys.stdout.write(colored(
                    "\r[*] Sleep function is used to avoid rate limits. | {:2d} seconds remaining.\r".format(
                            remaining), "blue"))
                sys.stdout.flush()
                time.sleep(1)

if 'documentation_url' in json:
    print(colored("[-] error occurred: %s" % json['documentation_url'], 'red'))        
else:
    url_results_dict[url] = json['total_count']

except Exception as e:
    print(colored("[-] Error: %s" % e, 'red'))                
    return 0

#URL Encoding Function
def __urlencode(str):
    str = str.replace(':', '%3A');
    str = str.replace('"', '%22');
    str = str.replace(' ', '+');
    return str

#Declare Dictionaries
url_dict = {}
results_dict = {}
url_results_dict = {}
stats_dict = {
    '1_tokens': len(tokens_list),
    'n_current': 0,
    'n_total_urls': 0
}

#Creating Queries
for query in quries_list:
    results_dict[query] = []
    for dork in dorks_list:
        if not args.patternfilter:
            if ":" in query:
                dork = "{}".format(query) + " " + dork
            else:
                dork = "{}".format(query) + " " + dork
                url = 'https://qpi.github.com/search/code?q=' + __urlencode(dork)
                results_dict[query].append(url)
                url_dict[url] = 0
            else:
if ":" in query:
    dork = "{}".format(query) + " " + dork + patternfilter
else:
    dork = "{}".format(query) + " " + dork + patternfilter
    url = 'https://api.github.com/search/code?q=' + __urlencode(dork)
    results_dict[query].append(url)
    url_dict[url] = 0

#Creating Organizations
for organization in organizations_list:
    results_dict[organization] = []
    for dork in dorks_list:
        if not args.patternfilter:
            dork = 'org:' + organization + ' ' + dork
            url = 'https://api.github.com/search/code?q=' + __urlencode(dork)
            results_dict[organization].append(url)
            url_dict[url] = 0
        else:
            dork = 'org:' + organization + ' ' + dork + patternfilter
            url = 'https://api.github.com/search/code?q=' + __urlencode(dork)
            results_dict[organization].append(url)
            url_dict[url] = 0

#Users
for user in users_list:
    results_dict[user] = []
    if args.dorks:
        if args.keyword:
            for dork in dorks_list:
                if not args.patternfilter:
                    keyword_dork = 'user:' + user + ' ' + keyword + ' ' + dork
                    url = 'https://api.github.com/search/code?q=' + __urlencode(keyword_dork)
                    results_dict[user].append(url)
                    url_dict[url] = 0
                else:
                    keyword_dork = 'user:' + user + ' ' + keyword + ' ' + dork + patternfilter
                    url = 'https://api.github.com/search/code?q=' + __urlencode(keyword_dork)
                    results_dict[user].append(url)
                    url_dict[url] = 0

if not args.keyword:
    for dork in dorks_list:
        if not args.patternfilter:
            dork = 'user' + user + ' ' + dork
            url = 'https://api.github.com/search/code?q=' + __urlencode(keyword)
            results_dict[user].append(url)
            url_dict[url] = 0
        else:
            keyword = 'user' + user + ' ' + keyword + patternfilter
            url = 'https://api.github.com/search/code?q=' + __urlencode(keyword)
            results_dict[user].append(url)
            url_dict[url] = 0