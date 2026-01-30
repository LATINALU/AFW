#!/usr/bin/env python3
"""
ATP v0.8.0+ - Tailwind CSS Diagnostic Script
============================================

Script para verificar la integración de Tailwind CSS y temas
"""

import requests
import re
from datetime import datetime

def check_frontend_health():
    """Verificar salud del frontend"""
    print("🔍 Verificando Frontend Health...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        print(f"✅ Frontend Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Verificar si contiene HTML
            if '<html' in content.lower():
                print("✅ Frontend Content: HTML válido")
            else:
                print("❌ Frontend Content: No es HTML válido")
                return False
                
            # Verificar si contiene Tailwind CSS
            if 'tailwind' in content.lower():
                print("✅ Tailwind CSS: Referenciado")
            else:
                print("⚠️ Tailwind CSS: No referenciado explícitamente")
            
            # Verificar si contiene globals.css
            if 'globals.css' in content.lower():
                print("✅ Globals CSS: Referenciado")
            else:
                print("⚠️ Globals CSS: No referenciado explícitamente")
            
            # Verificar si contiene themes.css
            if 'themes.css' in content.lower():
                print("✅ Themes CSS: Referenciado")
            else:
                print("⚠️ Themes CSS: No referenciado explícitamente")
            
            return True
        else:
            print(f"❌ Frontend Error: Status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Frontend Connection Error: {e}")
        return False

def check_css_variables():
    """Verificar variables CSS en el frontend"""
    print("\n🎨 Verificando Variables CSS...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        content = response.text
        
        # Buscar variables CSS
        css_vars = re.findall(r'--[\w-]+:\s*[^;]+', content)
        
        if css_vars:
            print(f"✅ Variables CSS encontradas: {len(css_vars)}")
            
            # Variables importantes
            important_vars = [
                '--background',
                '--foreground', 
                '--primary',
                '--secondary',
                '--muted',
                '--accent',
                '--destructive',
                '--border',
                '--input',
                '--ring'
            ]
            
            found_vars = []
            for var in important_vars:
                if any(var in css_var for css_var in css_vars):
                    found_vars.append(var)
            
            print(f"✅ Variables importantes encontradas: {len(found_vars)}/{len(important_vars)}")
            
            for var in found_vars:
                print(f"   - {var}")
                
            return len(found_vars) >= 8  # Al menos 8 de 10 variables importantes
        else:
            print("❌ No se encontraron variables CSS")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando variables CSS: {e}")
        return False

def check_theme_attributes():
    """Verificar atributos de tema"""
    print("\n🎭 Verificando Atributos de Tema...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        content = response.text
        
        # Buscar data-theme
        theme_attrs = re.findall(r'data-theme="([^"]+)"', content)
        
        if theme_attrs:
            print(f"✅ Atributos data-theme encontrados: {len(theme_attrs)}")
            
            for theme in set(theme_attrs):
                print(f"   - {theme}")
                
            # Verificar si executive está presente
            if 'executive' in theme_attrs:
                print("✅ Tema executive encontrado")
            else:
                print("❌ Tema executive no encontrado")
                
            return True
        else:
            print("❌ No se encontraron atributos data-theme")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando atributos de tema: {e}")
        return False

def check_tailwind_classes():
    """Verificar clases de Tailwind"""
    print("\n📝 Verificando Clases de Tailwind...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        content = response.text
        
        # Buscar clases de Tailwind comunes
        tailwind_classes = [
            'bg-background',
            'text-foreground',
            'bg-primary',
            'text-primary',
            'bg-card',
            'border-border',
            'bg-muted',
            'text-muted-foreground'
        ]
        
        found_classes = []
        for cls in tailwind_classes:
            if cls in content:
                found_classes.append(cls)
        
        print(f"✅ Clases Tailwind encontradas: {len(found_classes)}/{len(tailwind_classes)}")
        
        for cls in found_classes:
            print(f"   - {cls}")
            
        return len(found_classes) >= 6  # Al menos 6 de 8 clases importantes
        
    except Exception as e:
        print(f"❌ Error verificando clases Tailwind: {e}")
        return False

def check_css_imports():
    """Verificar imports de CSS"""
    print("\n📦 Verificando Imports de CSS...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        content = response.text
        
        # Buscar imports de CSS
        css_imports = re.findall(r'@import\s+["\']([^"\']+)["\']', content)
        
        if css_imports:
            print(f"✅ Imports CSS encontrados: {len(css_imports)}")
            
            for imp in css_imports:
                print(f"   - {imp}")
                
            # Verificar si themes.css está importado
            if any('themes.css' in imp for imp in css_imports):
                print("✅ themes.css importado")
            else:
                print("❌ themes.css no importado")
                
            return True
        else:
            print("❌ No se encontraron imports CSS")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando imports CSS: {e}")
        return False

def generate_css_test():
    """Generar HTML de prueba para CSS"""
    print("\n🧪 Generando Test CSS...")
    
    test_html = """
<!DOCTYPE html>
<html data-theme="executive">
<head>
    <title>ATP CSS Test</title>
    <style>
        /* Importar themes */
        @import '/styles/themes.css';
        
        /* Test styles */
        body {
            background: hsl(var(--background));
            color: hsl(var(--foreground));
            padding: 20px;
            font-family: Arial, sans-serif;
        }
        
        .test-card {
            background: hsl(var(--card));
            border: 1px solid hsl(var(--border));
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .test-button {
            background: hsl(var(--primary));
            color: hsl(var(--primary-foreground));
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            margin: 5px;
        }
        
        .test-button:hover {
            opacity: 0.8;
        }
        
        .theme-info {
            text-align: center;
            padding: 10px;
            background: hsl(var(--muted));
            border-radius: 6px;
            margin-top: 10px;
        }
        
        .color-preview {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin: 10px 0;
        }
        
        .color-dot {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            border: 1px solid rgba(255,255,255,0.2);
        }
    </style>
</head>
<body>
    <div class="theme-info">
        <h1>🎨 ATP CSS Test - Executive Theme</h1>
        <div class="color-preview">
            <div class="color-dot" style="background: hsl(var(--primary))"></div>
            <div class="color-dot" style="background: hsl(var(--accent))"></div>
            <div class="color-dot" style="background: hsl(var(--background))"></div>
        </div>
    </div>
    
    <div class="test-card">
        <h2 style="color: hsl(var(--primary))">Test Card</h2>
        <p style="color: hsl(var(--foreground))">Este es un test de las variables CSS del tema EXECUTIVE.</p>
        <button class="test-button">Botón Principal</button>
        <button class="test-button" style="background: hsl(var(--secondary))">Botón Secundario</button>
    </div>
    
    <div class="theme-info">
        <p><strong>Variables CSS Activas:</strong></p>
        <ul style="text-align: left; color: hsl(var(--muted-foreground));">
            <li>Primary: hsl(var(--primary))</li>
            <li>Background: hsl(var(--background))</li>
            <li>Card: hsl(var(--card))</li>
            <li>Border: hsl(var(--border))</li>
        </ul>
    </div>
    
    <script>
        // Test de cambio de tema
        const themes = ['executive', 'blueprint', 'iron-man', 'kawai', 'cyborg'];
        let currentTheme = 0;
        
        document.addEventListener('click', () => {
            currentTheme = (currentTheme + 1) % themes.length;
            const newTheme = themes[currentTheme];
            document.documentElement.setAttribute('data-theme', newTheme);
            document.querySelector('h1').textContent = `🎨 ATP CSS Test - ${newTheme.toUpperCase()} Theme`;
        });
    </script>
</body>
</html>
    """
    
    # Guardar archivo de prueba
    with open('css_test.html', 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    print("✅ Archivo css_test.html creado")
    print("   - Abre http://localhost:3000/css_test.html para probar")
    print("   - Haz clic para cambiar entre temas")
    
    return True

def main():
    """Función principal"""
    print("🚀 ATP v0.8.0+ - Tailwind CSS Diagnostic")
    print("=" * 50)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    tests = [
        ("Frontend Health", check_frontend_health),
        ("CSS Variables", check_css_variables),
        ("Theme Attributes", check_theme_attributes),
        ("Tailwind Classes", check_tailwind_classes),
        ("CSS Imports", check_css_imports),
        ("CSS Test Generator", generate_css_test)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"🧪 Ejecutando: {test_name}")
        print(f"{'='*50}")
        
        results[test_name] = test_func()
    
    # Resumen final
    print(f"\n{'='*50}")
    print("📊 RESUMEN DE DIAGNÓSTICO")
    print(f"{'='*50}")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<30} {status}")
    
    print(f"\n🎯 Resultado: {passed}/{total} tests pasaron")
    
    if passed == total:
        print("🎉 ¡Tailwind CSS está correctamente integrado!")
        print("🎨 Los temas deberían funcionar correctamente")
    else:
        print("⚠️ Hay problemas con la integración de Tailwind CSS")
        print("🔧 Revisa la configuración de CSS y temas")
    
    print(f"{'='*50}")
    
    return passed == total

if __name__ == "__main__":
    main()
