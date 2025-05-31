using System;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        var htmlFilePath = "htmlSourceDemo.html";
        var outputPdfPath = "output.pdf";
        var weasyPrintEndpoint = "http://localhost:5000/generate-pdf";

        if (!File.Exists(htmlFilePath))
        {
            Console.WriteLine($"File not found: {htmlFilePath}");
            return;
        }

        Console.WriteLine("Reading HTML content...");
        var html = await File.ReadAllTextAsync(htmlFilePath);

        Console.WriteLine("Sending HTML to PDF service...");
        using var httpClient = new HttpClient();
        using var content = new StringContent(html, Encoding.UTF8, "text/html");

        var response = await httpClient.PostAsync(weasyPrintEndpoint, content);
        if (!response.IsSuccessStatusCode)
        {
            Console.WriteLine($"PDF generation failed: {response.StatusCode}");
            return;
        }

        Console.WriteLine("Saving PDF to file...");
        var pdfBytes = await response.Content.ReadAsByteArrayAsync();
        await File.WriteAllBytesAsync(outputPdfPath, pdfBytes);

        Console.WriteLine($"PDF saved as: {outputPdfPath}");
    }
}
