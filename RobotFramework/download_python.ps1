$url = "https://sourceforge.net/projects/portable-python/files/latest/download"

$filename = "PortablePython.exe";

Write-Host "Downloading $filename (approx. 50MB)"

[Net.ServicePointManager]::SecurityProtocol = "tls12, tls11, tls"
Invoke-WebRequest -UserAgent "Wget" -Uri $url -OutFile $filename
