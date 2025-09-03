# Contributing to Financial AI Chatbot

¡Gracias por tu interés en contribuir a nuestro proyecto! Este documento te guiará paso a paso sobre cómo colaborar efectivamente en el desarrollo del Financial AI Chatbot.

## 📋 Tabla de Contenidos

- [Antes de Empezar](#antes-de-empezar)
- [Configuración Inicial](#configuración-inicial)
- [Workflow de Contribución](#workflow-de-contribución)
- [Estándares de Código](#estándares-de-código)
- [Proceso de Pull Request](#proceso-de-pull-request)
- [Estructura de Commits](#estructura-de-commits)
- [Testing](#testing)
- [Documentación](#documentación)
- [Resolución de Conflictos](#resolución-de-conflictos)
- [Comunicación y Colaboración](#comunicación-y-colaboración)

---

## 🚀 Antes de Empezar

### Prerrequisitos
- Python 3.9+
- Git configurado con tu nombre y email
- Docker y Docker Compose instalados
- Cuenta de GitHub con acceso al repositorio
- VS Code o tu editor preferido

### Estructura del Proyecto
Familiarízate con la organización del proyecto según el archivo `GUIA_PROYECTO.md`:
- **5 semanas de duración**
- **Equipo de 6-7 personas**
- **Arquitectura AWS ECS Container-Native**
- **Desarrollo local primero, luego AWS**

---

## ⚙️ Configuración Inicial

### 1. Fork y Clonado (si aplica)
```bash
# Clonar el repositorio principal
git clone https://github.com/EdissonMC/nasdaq-financial-advisor.git
cd nasdaq-financial-advisor

# Verificar ramas existentes
git branch -a
```

### 2. Configuración del Entorno Local
```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias (cuando estén disponibles)
pip install -r requirements.txt

# Copiar variables de entorno
cp .env.example .env
# Edita .env con tus credenciales
```

### 3. Verificar Docker Setup
```bash
# Verificar que Docker funciona
docker --version
docker-compose --version

# Levantar servicios locales (cuando estén configurados)
docker-compose up -d
```

---

## 🔄 Workflow de Contribución

### Estructura de Ramas Protegidas

#### **main** - Producción (ESTRICTAMENTE PROTEGIDA)
- ✅ Require PR before merging (mínimo 1 approval)
- ✅ Block force pushes
- ✅ Restrict deletions
- ✅ Linear history (opcional)
- ❌ Bypass para administradores

#### **develop** - Integración (PROTEGIDA PERO FLEXIBLE)
- ✅ Require PR before merging (mínimo 1 approval)
- ✅ Block force pushes
- ✅ Restrict deletions
- ❌ Include administrators (más flexible)

### 1. Crear Feature Branch

**SIEMPRE** crea una rama para tu feature desde `develop`:

```bash
# Actualizar develop
git checkout develop
git pull origin develop

# Crear tu feature branch
git checkout -b feature/nombre-descriptivo

# Ejemplos de nombres válidos:
# feature/data-pipeline-setup
# feature/pinecone-integration
# feature/streamlit-ui
# feature/docker-configuration
# bugfix/authentication-error
# hotfix/critical-memory-leak
```

### 2. Desarrollo en tu Branch

```bash
# Hacer cambios en tu código
# ... desarrollar ...

# Commits frecuentes y descriptivos
git add .
git commit -m "Add data extraction from PDF documents"

# Push a tu branch remota (backup)
git push origin feature/nombre-descriptivo
```

### 3. Mantener Branch Actualizada

```bash
# Diariamente, sincronizar con develop
git checkout develop
git pull origin develop
git checkout feature/nombre-descriptivo
git rebase develop

# Si hay conflictos, resolverlos y continuar
git add .
git rebase --continue

# Force push SOLO a tu feature branch
git push --force-with-lease origin feature/nombre-descriptivo
```

---

## 📝 Estándares de Código

### Python Style Guide
- Seguir **PEP 8**
- Usar **Black** para formatting automático
- **Isort** para imports organizados
- **Flake8** para linting

```bash
# Instalar herramientas de desarrollo
pip install black isort flake8 pytest

# Formatear código antes de commit
black .
isort .
flake8 .
```

### Estructura de Archivos
```python
# Ejemplo de estructura de archivo Python
"""
Module docstring: descripción clara del propósito.
"""

import os
import sys
from typing import List, Dict, Optional

import pandas as pd
import numpy as np
from fastapi import FastAPI

from services.search_service import SearchService
from utils.config import settings


class DocumentProcessor:
    """Class docstring: qué hace la clase."""
    
    def __init__(self, config: Dict[str, str]) -> None:
        self.config = config
    
    def process_document(self, file_path: str) -> Optional[Dict]:
        """
        Function docstring: qué hace, parámetros, retorno.
        
        Args:
            file_path: Ruta al archivo a procesar
            
        Returns:
            Diccionario con texto procesado o None si falla
        """
        # Implementación aquí
        pass
```

### Documentación de Código
- **Docstrings** en todas las funciones y clases
- **Type hints** en todas las funciones
- **Comments** para lógica compleja
- **README** por servicio cuando aplique

---

## 📋 Estructura de Commits

### Formato Obligatorio
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Tipos Válidos
- **feat**: Nueva funcionalidad
- **fix**: Corrección de bug
- **docs**: Cambios en documentación
- **style**: Formateo, espacios (no cambia lógica)
- **refactor**: Refactoring de código
- **test**: Agregar o modificar tests
- **chore**: Tareas de mantenimiento

### Ejemplos
```bash
feat(search): add semantic search with Pinecone integration

fix(api): resolve authentication timeout issue

docs(readme): update setup instructions for Docker

test(processor): add unit tests for PDF text extraction

refactor(llm): improve prompt template organization

chore(deps): update Python dependencies to latest versions
```

---

## 🔀 Proceso de Pull Request

### 1. Antes de Crear el PR

```bash
# Asegurar que el branch está actualizado
git checkout develop
git pull origin develop
git checkout feature/tu-branch
git rebase develop

# Ejecutar tests locales
pytest tests/
black . && isort . && flake8 .

# Push final
git push --force-with-lease origin feature/tu-branch
```

### 2. Crear Pull Request

Ve a GitHub y crea un PR desde tu `feature/branch` hacia `develop`.

**Template Obligatorio:**

```markdown
## 📝 Descripción
Brief description of what this PR does

## 🔧 Tipo de Cambio
- [ ] 🚀 Nueva funcionalidad (feat)
- [ ] 🐛 Corrección de bug (fix)
- [ ] 📚 Actualización de documentación (docs)
- [ ] 🎨 Mejoras de estilo/formateo (style)
- [ ] ♻️ Refactoring (refactor)
- [ ] ✅ Tests (test)
- [ ] 🔧 Tareas de mantenimiento (chore)

## 🧪 Testing
- [ ] Unit tests añadidos/actualizados
- [ ] Integration tests pasan
- [ ] Manual testing completado
- [ ] No hay regresiones

## 📋 Checklist
- [ ] Código sigue las guidelines del proyecto
- [ ] Self-review completado
- [ ] Documentación actualizada si es necesario
- [ ] No hay merge conflicts
- [ ] Commits siguien el formato convencional
- [ ] Branch está actualizado con develop

## 🔗 Issues Relacionados
Closes #issue_number (si aplica)

## 📸 Screenshots (si aplica)
[Screenshots de UI changes]

## 🔍 Notas para el Reviewer
[Anything specific the reviewer should focus on]
```

### 3. Code Review Process

#### Para el Author:
1. **Crear PR** con descripción detallada
2. **Asignar reviewers** (mínimo 1 persona del equipo)
3. **Responder feedback** de forma constructiva
4. **Hacer changes** según comentarios
5. **Re-request review** después de cambios

#### Para el Reviewer:
1. **Review code** en máximo 72 horas
2. **Dar feedback constructivo** y específico
3. **Sugerir mejoras** con ejemplos
4. **Aprobar** cuando esté listo
5. **No hacer merge** directo (solo el autor o lead)

### 4. Merge del PR

**Solo el autor del PR o el project lead puede hacer merge.**

Opciones de merge:
- **Squash and merge** (PREFERIDO): Para features completas
- **Rebase and merge**: Para historiales limpios
- **Create merge commit**: Solo para releases

---

## 🧪 Testing

### Estructura de Tests
```
tests/
├── unit/
│   ├── test_document_processor.py
│   ├── test_search_service.py
│   └── test_llm_service.py
├── integration/
│   ├── test_api_endpoints.py
│   └── test_rag_pipeline.py
└── fixtures/
    ├── sample_documents.pdf
    └── mock_responses.json
```

### Escribir Tests
```python
# tests/unit/test_document_processor.py
import pytest
from services.document_processor import DocumentProcessor

class TestDocumentProcessor:
    def setup_method(self):
        self.processor = DocumentProcessor(config={})
    
    def test_extract_text_from_pdf(self):
        """Test PDF text extraction functionality."""
        result = self.processor.extract_text("tests/fixtures/sample.pdf")
        assert result is not None
        assert len(result) > 0
        assert isinstance(result, str)
    
    def test_chunk_text_with_overlap(self):
        """Test text chunking with overlap."""
        text = "This is a long text that needs to be chunked."
        chunks = self.processor.chunk_text(text, chunk_size=20, overlap=5)
        assert len(chunks) > 1
        assert all(len(chunk) <= 20 for chunk in chunks)
```

### Ejecutar Tests
```bash
# Todos los tests
pytest

# Tests específicos
pytest tests/unit/

# Con coverage
pytest --cov=services --cov-report=html

# Tests en paralelo
pytest -n auto
```

---

## 📚 Documentación

### README por Servicio
Cada servicio debe tener su propio README:
```
services/
├── search-service/
│   ├── README.md
│   ├── app/
│   └── tests/
└── llm-service/
    ├── README.md
    ├── app/
    └── tests/
```

### API Documentation
- Usar **FastAPI** auto-docs cuando sea posible
- Documentar endpoints con ejemplos
- Incluir schemas de request/response

### Code Comments
```python
# ✅ Good comment
def calculate_similarity_score(query_vector: List[float], doc_vector: List[float]) -> float:
    """
    Calculate cosine similarity between query and document vectors.
    Used for ranking search results by relevance.
    """
    # Normalize vectors to handle different magnitudes
    query_norm = np.linalg.norm(query_vector)
    doc_norm = np.linalg.norm(doc_vector)
    
    # Return cosine similarity score (0-1 range)
    return np.dot(query_vector, doc_vector) / (query_norm * doc_norm)

# ❌ Bad comment
def calc_sim(q, d):  # calculate similarity
    # do math
    return np.dot(q, d) / (np.linalg.norm(q) * np.linalg.norm(d))
```

---

## 🔧 Resolución de Conflictos

### Merge Conflicts
```bash
# Cuando aparezcan conflictos durante rebase
git status  # Ver archivos en conflicto

# Editar archivos manualmente, buscar:


# Después de resolver
git add archivo_resuelto.py
git rebase --continue

# Si te confundes, puedes abortar
git rebase --abort
```

### Conflictos Comunes
1. **Import statements**: Organizar alfabéticamente
2. **Dependencies**: Mantener versiones compatibles
3. **Configuration files**: Coordinar con el equipo
4. **Database schemas**: Discutir cambios primero

---

## 💬 Comunicación y Colaboración

### Daily Standups
- **Duración**: 15 minutos máximo
- **Formato**: ¿Qué hiciste ayer? ¿Qué harás hoy? ¿Hay blockers?
- **Herramienta**: Slack/Discord/Teams

### Code Reviews
- **Ser constructivo**, no crítico
- **Sugerir mejoras** con ejemplos
- **Aprobar rápidamente** si está bien
- **Hacer preguntas** para entender el código

### Issues y Bugs
- Usar **GitHub Issues** para tracking
- **Labels** apropiados: bug, enhancement, documentation
- **Asignar** a la persona responsable
- **Cerrar** cuando esté resuelto

### Comunicación de Cambios
- **Slack/Discord** para comunicación diaria
- **GitHub Discussions** para decisiones técnicas
- **PRs** para cambios de código
- **Wiki** para documentación que perdura

---

## 📊 Métricas y Calidad

### Definition of Done
Una feature está "Done" cuando:
- [ ] Código escrito y funcionando
- [ ] Tests unitarios pasando
- [ ] Integration tests pasando
- [ ] Code review aprobado
- [ ] Documentación actualizada
- [ ] No hay regresiones
- [ ] PR merged a develop

### Métricas del Equipo
- **Velocity**: Features completadas por sprint
- **Quality**: Bugs por feature
- **Review time**: Tiempo promedio de code review
- **Test coverage**: Porcentaje de código cubierto

---

## 🚨 Guía de Emergencias

### Hotfixes Críticos
```bash
# Para bugs críticos en main
git checkout main
git pull origin main
git checkout -b hotfix/critical-issue

# Fix rápido
git commit -m "hotfix: resolve critical authentication bypass"
git push origin hotfix/critical-issue

# PR directo a main (excepcional)
# Después merge back a develop
```

### Rollback de Changes
```bash
# Revertir merge específico
git revert -m 1 <merge-commit-hash>

# Revertir último commit
git revert HEAD

# Reset completo (cuidado!)
git reset --hard HEAD~1
```

---


*Última actualización: Septiembre 2025*
