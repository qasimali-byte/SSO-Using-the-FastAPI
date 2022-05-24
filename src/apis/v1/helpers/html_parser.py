from bs4 import BeautifulSoup
import re

class HTMLPARSER():

    @staticmethod
    def parse_html(html_string):
        
#         html_string = '''<!DOCTYPE html>
# <html>
#   <head>
#     <meta charset="utf-8" />
#   </head>
#   <body onload="document.forms[0].submit()">
#     <noscript>
#       <p>
#         <strong>Note:</strong>
#         Since your browser does not support JavaScript,
#         you must press the Continue button once to proceed.
#       </p>
#     </noscript>
#     <form action="http://localhost:8000/sso/acs" method="post">
#       <input type="hidden" name="SAMLResponse" value="PG5zMDpSZXNwb25zZSB4bWxuczpuczA9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpwcm90b2NvbCIgeG1sbnM6bnMxPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIiB4bWxuczp4c2k9Imh0dHA6Ly93d3cudzMub3JnLzIwMDEvWE1MU2NoZW1hLWluc3RhbmNlIiBJRD0iaWQtUER0TVFZSEYzTmxnTDlFZTIiIEluUmVzcG9uc2VUbz0iaWQtTlFzV3RZNUhCbDJCNWZNU0IiIFZlcnNpb249IjIuMCIgSXNzdWVJbnN0YW50PSIyMDIyLTA1LTIzVDE4OjUwOjMwWiIgRGVzdGluYXRpb249Imh0dHA6Ly9sb2NhbGhvc3Q6ODAwMC9zc28vYWNzIj48bnMxOklzc3VlciBGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpuYW1laWQtZm9ybWF0OmVudGl0eSIgLz48bnMwOlN0YXR1cz48bnMwOlN0YXR1c0NvZGUgVmFsdWU9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpzdGF0dXM6U3VjY2VzcyIgLz48L25zMDpTdGF0dXM+PG5zMTpBc3NlcnRpb24gVmVyc2lvbj0iMi4wIiBJRD0iaWQtSlVnOEN4SnNQMTNVYVE1cFciIElzc3VlSW5zdGFudD0iMjAyMi0wNS0yM1QxODo1MDozMFoiPjxuczE6SXNzdWVyIEZvcm1hdD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOm5hbWVpZC1mb3JtYXQ6ZW50aXR5IiAvPjxuczE6U3ViamVjdD48bnMxOk5hbWVJRCBOYW1lUXVhbGlmaWVyPSJmb28iIEZvcm1hdD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOm5hbWVpZC1mb3JtYXQ6dHJhbnNpZW50Ij5zeWVkQGdtYWlsLmNvbTwvbnMxOk5hbWVJRD48bnMxOlN1YmplY3RDb25maXJtYXRpb24gTWV0aG9kPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6Y206YmVhcmVyIj48bnMxOlN1YmplY3RDb25maXJtYXRpb25EYXRhIE5vdE9uT3JBZnRlcj0iMjAyMi0wNS0yM1QxOTo1MDozMFoiIFJlY2lwaWVudD0iaHR0cDovL2xvY2FsaG9zdDo4MDAwL3Nzby9hY3MiIEluUmVzcG9uc2VUbz0iaWQtTlFzV3RZNUhCbDJCNWZNU0IiIC8+PC9uczE6U3ViamVjdENvbmZpcm1hdGlvbj48L25zMTpTdWJqZWN0PjxuczE6Q29uZGl0aW9ucyBOb3RCZWZvcmU9IjIwMjItMDUtMjNUMTg6NTA6MzBaIiBOb3RPbk9yQWZ0ZXI9IjIwMjItMDUtMjNUMTk6NTA6MzBaIj48bnMxOkF1ZGllbmNlUmVzdHJpY3Rpb24+PG5zMTpBdWRpZW5jZT5sb2FkYmFsYW5jZXItOS5zaXJvZS5jb208L25zMTpBdWRpZW5jZT48L25zMTpBdWRpZW5jZVJlc3RyaWN0aW9uPjwvbnMxOkNvbmRpdGlvbnM+PG5zMTpBdHRyaWJ1dGVTdGF0ZW1lbnQ+PG5zMTpBdHRyaWJ1dGUgTmFtZT0ibmFtZSIgTmFtZUZvcm1hdD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmF0dHJuYW1lLWZvcm1hdDp1cmkiPjxuczE6QXR0cmlidXRlVmFsdWUgeHNpOnR5cGU9InhzOnN0cmluZyIgeG1sbnM6eHM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDEvWE1MU2NoZW1hIiAvPjwvbnMxOkF0dHJpYnV0ZT48bnMxOkF0dHJpYnV0ZSBOYW1lPSJ1cm46b2lkOjEuMi44NDAuMTEzNTQ5LjEuOS4xLjEiIE5hbWVGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphdHRybmFtZS1mb3JtYXQ6dXJpIiBGcmllbmRseU5hbWU9ImVtYWlsIj48bnMxOkF0dHJpYnV0ZVZhbHVlIHhzaTp0eXBlPSJ4czpzdHJpbmciIHhtbG5zOnhzPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxL1hNTFNjaGVtYSI+c3llZEBnbWFpbC5jb208L25zMTpBdHRyaWJ1dGVWYWx1ZT48L25zMTpBdHRyaWJ1dGU+PC9uczE6QXR0cmlidXRlU3RhdGVtZW50PjwvbnMxOkFzc2VydGlvbj48L25zMDpSZXNwb25zZT4="/>
#       <input type="hidden" name="RelayState" value="/whoami"/>
#       <noscript>
#         <input type="submit" value="Continue"/>
#       </noscript>
#     </form>
#   </body>
# </html>'''
        soup = BeautifulSoup(html_string, 'html.parser')
        url = soup.find('form').get('action')
        saml_resp = soup.find('input', attrs={'name':re.compile(r'SAMLResponse')}).get('value')
        return url,saml_resp


# HTMLPARSER().parse_html(html_string="")