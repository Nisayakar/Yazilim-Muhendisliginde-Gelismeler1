import asyncio
import sys
import os
import datetime
import time
import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

REPORT_DIR = "/app/reports"
ai_client = ollama.Client(host='http://ollama:11434')

async def generate_report():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    report_file = os.path.join(REPORT_DIR, f"library_report_{today}.md")
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["mcp_server.py"],
        env=dict(os.environ)
    )

    print("Ajan iş başında...")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
  
            stats = await session.call_tool("get_system_stats")
            search_res = await session.call_tool("search_library", arguments={"keyword": "a"}) # Örnek arama
            
            raw_data = f"{stats.content[0].text}\n\nÖrnek Kitap Taraması:\n{search_res.content[0].text}"
            
        
            prompt = f"""
            Sen bir kütüphane yöneticisisin. Aşağıdaki sistem verilerini analiz et ve bir rapor yaz.
            
            Veriler:
            {raw_data}
            
            Rapor Formatı:
            1. Genel Durum Özeti
            2. Kitap/Kullanıcı Oranı Analizi
            3. Öneriler (Daha fazla kitap alınmalı mı?)
            4. Türkçe olsun ve Markdown formatında yaz.
            """
            
            try:
                response = ai_client.chat(model='gemma:2b', messages=[{'role': 'user', 'content': prompt}])
                content = response['message']['content']
                
                if not os.path.exists(REPORT_DIR):
                    os.makedirs(REPORT_DIR)
                    
                with open(report_file, "w", encoding="utf-8") as f:
                    f.write(f"# 📚 Kütüphane Günlük Raporu ({today})\n\n{content}")
                    
                print(f"Rapor oluşturuldu: {report_file}")
            except Exception as e:
                print(f"AI Hatası: {e}")

if __name__ == "__main__":

    print("Sistem açılıyor... (20sn bekleme)")
    time.sleep(20)
    
    while True:
        asyncio.run(generate_report())
        print("Ajan uykuya dalıyor (1 saat)...")
        time.sleep(3600)