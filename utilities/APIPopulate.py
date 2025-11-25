import json
from textwrap import indent

# Input/Output paths
INPUT_JSON = "/Users/Henry/Desktop/NEAComputerScience/SimulationAPI/swagger.json"
OUTPUT_TEX = "/Users/Henry/Desktop/CompSciNEA/ComputerScienceNEAReport/Chapters/TechnicalSolutionMedia/APIDocs.tex"

# Color scheme for different HTTP methods
METHOD_COLORS = {
    "get": "blue",
    "post": "green",
    "put": "orange",
    "delete": "red",
    "patch": "purple"
}

# Background colors for endpoint boxes
METHOD_BG_COLORS = {
    "get": "blue!5",
    "post": "green!5",
    "put": "orange!5",
    "delete": "red!5",
    "patch": "purple!5"
}

def tex_escape(text: str) -> str:
    """Escape LaTeX special characters."""
    if not text:
        return ""
    replacements = {
        "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
        "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}", "\\": r"\textbackslash{}"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def get_method_color(method: str) -> str:
    """Get the color for a specific HTTP method."""
    return METHOD_COLORS.get(method.lower(), "gray")

def get_method_bg_color(method: str) -> str:
    """Get the background color for a specific HTTP method."""
    return METHOD_BG_COLORS.get(method.lower(), "gray!5")

def resolve_schema_properties(schema_ref: str, schemas: dict) -> dict:
    """Resolve a $ref to get the actual schema properties."""
    if not schema_ref or not schema_ref.startswith("#/components/schemas/"):
        return {}
    
    schema_name = schema_ref.split("/")[-1]
    schema = schemas.get(schema_name, {})
    return schema.get("properties", {})

def generate_endpoint_tex(method: str, path: str, data: dict, schemas: dict) -> str:
    """Generate LaTeX for a single endpoint with enhanced visual styling."""
    tex = []
    summary = tex_escape(data.get("summary", ""))
    description = tex_escape(data.get("description", ""))
    method_upper = method.upper()
    method_color = get_method_color(method)
    method_bg_color = get_method_bg_color(method)
    
    # Create a colored box for the endpoint
    tex.append("\\begin{tcolorbox}[")
    tex.append(f"    colback={method_bg_color},")
    tex.append(f"    colframe={method_color},")
    tex.append("    arc=2mm,")
    tex.append("    boxrule=1pt,")
    tex.append("    left=5pt,")
    tex.append("    right=5pt,")
    tex.append("    top=5pt,")
    tex.append("    bottom=5pt")
    tex.append("]")
    
    # Method and path header with colored badge
    tex.append(f"\\noindent\\colorbox{{{method_color}}}{{\\textcolor{{white}}{{\\textbf{{{method_upper}}}}}}} ")
    tex.append(f"\\texttt{{\\large {tex_escape(path)}}}\\\\[0.3em]")
    
    # Summary
    if summary:
        tex.append(f"\\textit{{{summary}}}\\\\[0.3em]")
    
    # Description
    if description:
        tex.append(f"\\textbf{{Description:}} {description}\\\\[0.5em]")

    # Parameters
    params = data.get("parameters", [])
    if params:
        tex.append("\\vspace{0.3em}")
        tex.append("\\textbf{\\textcolor{blue}{Parameters:}}\\\\[0.2em]")
        tex.append("\\begin{tabular}{|l|l|l|}")
        tex.append("\\hline")
        tex.append("\\rowcolor{gray!20}")
        tex.append("\\textbf{Name} & \\textbf{Location} & \\textbf{Type} \\\\ \\hline")
        for i, p in enumerate(params):
            name = tex_escape(p.get("name", ""))
            loc = tex_escape(p.get("in", ""))
            typ = tex_escape(p.get("schema", {}).get("type", ""))
            # Alternate row colors
            if i % 2 == 1:
                tex.append("\\rowcolor{gray!5}")
            tex.append(f"\\texttt{{{name}}} & {loc} & \\texttt{{{typ}}} \\\\ \\hline")
        tex.append("\\end{tabular}\\\\[0.5em]")

    # Request body
    if "requestBody" in data:
        tex.append("\\vspace{0.3em}")
        tex.append("\\textbf{\\textcolor{green}{Request Body:}}\\\\[0.2em]")
        try:
            schema_ref = (
                data["requestBody"]["content"]
                .get("application/json", {})
                .get("schema", {})
                .get("$ref", "")
            )
            if schema_ref:
                ref_name = schema_ref.split("/")[-1]
                tex.append(f"Schema: \\texttt{{{ref_name}}}\\\\[0.3em]")
                
                # Get the schema properties
                properties = resolve_schema_properties(schema_ref, schemas)
                if properties:
                    tex.append("\\begin{tabular}{|l|l|l|}")
                    tex.append("\\hline")
                    tex.append("\\rowcolor{green!10}")
                    tex.append("\\textbf{Property} & \\textbf{Type} & \\textbf{Nullable} \\\\ \\hline")
                    for i, (prop_name, prop_data) in enumerate(properties.items()):
                        prop_type = prop_data.get("type", "")
                        prop_format = prop_data.get("format", "")
                        nullable = prop_data.get("nullable", False)
                        
                        # Build type string
                        if prop_format:
                            type_str = f"{prop_type} ({prop_format})"
                        else:
                            type_str = prop_type
                        
                        nullable_str = "Yes" if nullable else "No"
                        
                        if i % 2 == 1:
                            tex.append("\\rowcolor{gray!5}")
                        tex.append(f"\\texttt{{{tex_escape(prop_name)}}} & {tex_escape(type_str)} & {nullable_str} \\\\ \\hline")
                    tex.append("\\end{tabular}\\\\[0.5em]")
        except Exception:
            pass

    # Responses
    responses = data.get("responses", {})
    if responses:
        tex.append("\\vspace{0.3em}")
        tex.append("\\textbf{\\textcolor{purple}{Responses:}}\\\\[0.2em]")
        tex.append("\\begin{tabular}{|c|p{10cm}|}")
        tex.append("\\hline")
        tex.append("\\rowcolor{gray!20}")
        tex.append("\\textbf{Status Code} & \\textbf{Description} \\\\ \\hline")
        for i, (code, resp) in enumerate(responses.items()):
            desc = tex_escape(resp.get("description", ""))
            # Color code based on status
            if code.startswith("2"):
                code_color = "green!20"
            elif code.startswith("4"):
                code_color = "orange!20"
            elif code.startswith("5"):
                code_color = "red!20"
            else:
                code_color = "gray!20"
            
            if i % 2 == 1:
                tex.append("\\rowcolor{gray!5}")
            tex.append(f"\\colorbox{{{code_color}}}{{\\textbf{{{code}}}}} & {desc} \\\\ \\hline")
        tex.append("\\end{tabular}")

    tex.append("\\end{tcolorbox}")
    tex.append("\\vspace{0.5em}")
    return "\n".join(tex)

def main():
    with open(INPUT_JSON, "r") as f:
        swagger = json.load(f)

    # Extract API info
    api_info = swagger.get("info", {})
    api_title = tex_escape(api_info.get("title", "API Documentation"))
    api_description = tex_escape(api_info.get("description", ""))
    api_version = tex_escape(api_info.get("version", ""))
    
    # Get schemas from components
    schemas = swagger.get("components", {}).get("schemas", {})
    
    paths = swagger.get("paths", {})
    grouped = {}
    for path, methods in paths.items():
        for method, data in methods.items():
            tag = data.get("tags", ["Misc"])[0]
            grouped.setdefault(tag, []).append((method, path, data))

    # Start building the LaTeX document
    tex_sections = []
    
    
    # Main section header with banner
    tex_sections.append("\\section{API Documentation}")
    tex_sections.append("")
    
    # API Information Banner
 
    tex_sections.append("This section documents the RESTful API endpoints for the epidemic simulation system. ")
    tex_sections.append("The API follows standard HTTP methods and returns JSON responses. ")
    tex_sections.append("All endpoints require authentication unless otherwise specified.")
    tex_sections.append("\\vspace{1em}")
    
    # Legend for HTTP methods
    tex_sections.append("\\subsection*{HTTP Method Legend}")
    tex_sections.append("\\begin{tcolorbox}[colback=gray!5, colframe=gray!50, arc=2mm]")
    tex_sections.append("\\begin{tabular}{ll}")
    for method, color in METHOD_COLORS.items():
        tex_sections.append(f"\\colorbox{{{color}}}{{\\textcolor{{white}}{{\\textbf{{{method.upper()}}}}}}} & "
                          f"{method.upper()} operation \\\\[0.2em]")
    tex_sections.append("\\end{tabular}")
    tex_sections.append("\\end{tcolorbox}")
    tex_sections.append("\\vspace{1.5em}")

    # Generate sections for each tag
    for tag, endpoints in sorted(grouped.items()):
        tex_sections.append(f"\\subsection{{{tex_escape(tag)} Endpoints}}")
        tex_sections.append("")
        
        # Add a colored divider
        tex_sections.append("\\noindent\\textcolor{gray!60}{\\rule{\\linewidth}{0.5pt}}")
        tex_sections.append("\\vspace{0.5em}")
        tex_sections.append("")
        
        for method, path, data in sorted(endpoints, key=lambda x: (x[1], x[0])):
            tex_sections.append(generate_endpoint_tex(method, path, data, schemas))
            tex_sections.append("")

    # Write to file
    with open(OUTPUT_TEX, "w") as f:
        f.write("\n".join(tex_sections))

    print(f"✓ Enhanced LaTeX API documentation written to {OUTPUT_TEX}")
    print(f"  • {len(grouped)} endpoint categories")
    print(f"  • {sum(len(eps) for eps in grouped.values())} total endpoints")

if __name__ == "__main__":
    main()