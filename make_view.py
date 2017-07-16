import sys
import re
import json

from jinja2 import Template

template = Template ("""
<!Doctype html>
<html>
    <head>
        <title>Pylint webview</title>
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    </head>
    <body>
        <header class="w3-container">
            <h1>Pylint webview</h1>
        </header>
	<nav class="w3-sidebar w3-bar-block w3-border" style="width:40%">
	  <strong>ISSUES: {{ num_issues }}</strong>
      <div>
            <ul class="w3-ul w3-card-4 w3-hoverable">
	            {{ issues }}
            </ul>
      </div>
	</nav>
    <div class="content w3-panel w3-border w3-round-xlarge" style="margin-left:40%">
        <div id="symbol" class="w3-container w3-green w3-xxlarge"></div>
        <div id="type" class="w3-container" ></div>
        <div id="path" class="w3-container"></div>
        <div id="module" class="w3-container"></div>
        <div id="place" class="w3-container"></div>
        <div id="message" class="w3-topbar w3-margin w3-large w3-container"></div>
        
    </div>
    <script>
        var issues_data = {{ json_data }}
        function show_issue(id) {
            document.getElementById("symbol").innerHTML = 
                issues_data[id]['symbol'];
            document.getElementById("type").innerHTML = 
                "Type: " + issues_data[id]['type']
            document.getElementById("path").innerHTML = 
                "Path: " + issues_data[id]['path'];
            document.getElementById("module").innerHTML = 
                "Module: " + issues_data[id]['module'];
            document.getElementById("place").innerHTML = 
                "Line: " + issues_data[id]['line']
                + " Column: " + issues_data[id]['column']
            document.getElementById("message").innerHTML = 
                issues_data[id]['message'];
            
        }
    </script>
    </body>
</html>
""")


def make_entry(json_data, entry_number):
    entry_text = json_data["message"]
    found = re.search("\n", entry_text)
    if found:
        limit = found.span()[0]
        entry_text = entry_text[:limit]
    entry = "<li id=\"element_{}\" onclick=\"show_issue({})\">{}</li>".format(\
                entry_number, entry_number, entry_text)
    return entry

def make_list(issues_list):
    entries = []
    entry_number = 0
    for issue in issues_list:
        entries.append(make_entry(issue, entry_number))
        entry_number += 1
    return str.join("\n", entries)

if __name__ == "__main__":
    with open(sys.argv[1]) as data_file:
        json_data = json.load(data_file)

    issues_list = make_list(json_data)
    print(template.render(\
                issues=issues_list, \
                json_data=str(json_data),
                num_issues=len(json_data)))
    
