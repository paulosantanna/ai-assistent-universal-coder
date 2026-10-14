const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const DIAGRAMS_DIR = path.resolve(process.argv[2] || './diagrams');
const SRC_DIR = path.join(DIAGRAMS_DIR, 'src');
const SVG_DIR = path.join(DIAGRAMS_DIR, 'svg');
const PNG_DIR = path.join(DIAGRAMS_DIR, 'png');

const DIAGRAMS = {
  'system-architecture': generateSystemArchitecture,
  'infrastructure': generateInfrastructure,
  'data-flow': generateDataFlow,
  'entity-relationship': generateEntityRelationship,
  'mongodb-schema': generateMongoDBSchema,
  'chromadb-collections': generateChromaDBCollections,
  'api-route-map': generateAPIRouteMap,
  'component-diagram': generateComponentDiagram,
  'sequence-diagram': generateSequenceDiagram,
  'deployment': generateDeployment,
  'security-architecture': generateSecurityArchitecture,
  'integration-map': generateIntegrationMap,
  'improvement-roadmap': generateImprovementRoadmap,
  'project-mindmap': generateProjectMindmap
};

function main() {
  [SRC_DIR, SVG_DIR, PNG_DIR].forEach(d => fs.mkdirSync(d, { recursive: true }));

  const projectData = process.argv[3] ? JSON.parse(process.argv[3]) : {};

  Object.entries(DIAGRAMS).forEach(([name, generator]) => {
    const mmd = generator(projectData);
    const mmdPath = path.join(SRC_DIR, `${name}.mmd`);
    fs.writeFileSync(mmdPath, mmd, 'utf-8');
    console.log(`Generated: ${name}.mmd`);
  });

  // Export to SVG and PNG using mmdc
  try {
    execSync('npx --yes @mermaid-js/mermaid-cli --version', { stdio: 'pipe' });
    fs.readdirSync(SRC_DIR).forEach(file => {
      if (!file.endsWith('.mmd')) return;
      const base = path.basename(file, '.mmd');
      const src = path.join(SRC_DIR, file);
      const svg = path.join(SVG_DIR, `${base}.svg`);
      const png = path.join(PNG_DIR, `${base}.png`);
      try {
        execSync(`npx mmdc -i "${src}" -o "${svg}" -b white`, { stdio: 'pipe' });
        execSync(`npx mmdc -i "${src}" -o "${png}" -b white`, { stdio: 'pipe' });
        console.log(`Exported: ${base}.svg + ${base}.png`);
      } catch (e) {
        console.error(`Failed to export ${base}: ${e.message}`);
      }
    });
  } catch (e) {
    console.error('mmdc not available. Mermaid source files generated but not exported.');
  }
}

function generateSystemArchitecture(data) {
  const layers = data.layers || {};
  return `graph TB
    subgraph Presentation["Presentation Layer"]
        FE[Frontend App]
    end
    subgraph API["API / Backend Layer"]
        GW[API Gateway / Load Balancer]
        API1[Service A]
        API2[Service B]
        API3[Service C]
    end
    subgraph Data["Data Layer"]
        MDB[(MongoDB)]
        CDB[(ChromaDB)]
        SQL[(PostgreSQL)]
    end
    subgraph Infra["Infrastructure Layer"]
        K8S[Kubernetes]
        DKR[Docker]
        CLD[Cloud Provider]
    end
    subgraph Integration["Integration Layer"]
        EXT[External APIs]
        MCP[MCP Servers]
        Q[Message Queue]
    end
    subgraph Security["Security Layer"]
        AUTH[Auth Provider]
        VAULT[Secrets Manager]
    end
    FE --> GW
    GW --> API1 & API2 & API3
    API1 --> MDB & SQL
    API2 --> CDB
    API3 --> EXT & MCP & Q
    API1 & API2 & API3 --> AUTH
    K8S --> DKR
    CLD --> K8S
    VAULT --> API1 & API2 & API3`;
}

function generateInfrastructure(data) {
  return `graph TB
    subgraph Production["Production Environment"]
        subgraph K8S["Kubernetes Cluster"]
            POD1[Pod: API Server]
            POD2[Pod: Worker]
            POD3[Pod: Frontend]
            SVC1[Service: api-svc]
            SVC2[Service: frontend-svc]
            INGRESS[Ingress Controller]
        end
        REG[Container Registry]
        LB[Load Balancer]
    end
    subgraph Staging["Staging Environment"]
        K8S_STG[Kubernetes Cluster - Staging]
    end
    subgraph Dev["Development"]
        LOCAL[Docker Compose]
    end
    DNS[DNS] --> LB
    LB --> INGRESS
    INGRESS --> SVC1 & SVC2
    SVC1 --> POD1
    SVC2 --> POD3
    POD1 & POD2 --> REG`;
}

function generateDataFlow(data) {
  return `flowchart LR
    USER[User / Client]
    REQ[HTTP Request]
    AUTH[Auth Middleware]
    ROUTE[Router]
    CTRL[Controller]
    SVC[Service Layer]
    VAL[Validation]
    DB[(Database)]
    CACHE[(Cache)]
    EXT[External API]
    RESP[JSON Response]

    USER --> REQ
    REQ --> AUTH
    AUTH --> ROUTE
    ROUTE --> CTRL
    CTRL --> VAL
    VAL --> SVC
    SVC <--> DB
    SVC <--> CACHE
    SVC --> EXT
    SVC --> RESP
    RESP --> USER`;
}

function generateEntityRelationship(data) {
  return `erDiagram
    USER ||--o{ ORDER : places
    USER {
        string id PK
        string name
        string email
        datetime createdAt
    }
    ORDER ||--|{ ORDER_ITEM : contains
    ORDER {
        string id PK
        string userId FK
        decimal total
        string status
        datetime createdAt
    }
    ORDER_ITEM ||--|| PRODUCT : references
    ORDER_ITEM {
        string id PK
        string orderId FK
        string productId FK
        int quantity
        decimal price
    }
    PRODUCT {
        string id PK
        string name
        string description
        decimal price
        int stock
    }
    PRODUCT ||--o{ CATEGORY : belongsTo
    CATEGORY {
        string id PK
        string name
        string slug
    }`;
}

function generateMongoDBSchema(data) {
  return `graph TB
    subgraph MongoDB["MongoDB Database"]
        subgraph Collections["Collections"]
            USERS[users]
            PRODUCTS[products]
            ORDERS[orders]
            CATEGORIES[categories]
            SESSIONS[sessions]
            AUDIT_LOGS[audit_logs]
        end
        subgraph Indexes["Indexes"]
            IDX1["users.email (unique)"]
            IDX2["orders.userId"]
            IDX3["products.categoryId"]
            IDX4["sessions.expiresAt (TTL)"]
        end
    end
    USERS --> IDX1
    ORDERS --> IDX2
    PRODUCTS --> IDX3
    SESSIONS --> IDX4
    USERS -.- ORDERS
    PRODUCTS -.- CATEGORIES
    ORDERS -.- PRODUCTS`;
}

function generateChromaDBCollections(data) {
  return `graph TB
    subgraph ChromaDB["ChromaDB Vector Database"]
        COLL1[Collection: documents]
        COLL2[Collection: embeddings]
        COLL3[Collection: code_vectors]
    end
    subgraph Metadata["Collection Metadata"]
        META1["documents: dim=1536, distance=cosine"]
        META2["embeddings: dim=768, distance=cosine"]
        META3["code_vectors: dim=1536, distance=cosine"]
    end
    COLL1 --- META1
    COLL2 --- META2
    COLL3 --- META3
    subgraph UseCases["Use Cases"]
        UC1["RAG - Question Answering"]
        UC2["Semantic Search"]
        UC3["Code Similarity"]
    end
    META1 --- UC1
    META2 --- UC2
    META3 --- UC3`;
}

function generateAPIRouteMap(data) {
  return `graph LR
    subgraph Routes["API Routes"]
        direction LR
        subgraph Auth["Auth Endpoints"]
            POST_LOGIN["POST /api/auth/login"]
            POST_REGISTER["POST /api/auth/register"]
            POST_LOGOUT["POST /api/auth/logout"]
            POST_REFRESH["POST /api/auth/refresh"]
        end
        subgraph Users["User Endpoints"]
            GET_USERS["GET /api/users"]
            GET_USER["GET /api/users/:id"]
            PUT_USER["PUT /api/users/:id"]
            DEL_USER["DELETE /api/users/:id"]
        end
        subgraph Products["Product Endpoints"]
            GET_PRODS["GET /api/products"]
            GET_PROD["GET /api/products/:id"]
            POST_PROD["POST /api/products"]
            PUT_PROD["PUT /api/products/:id"]
        end
        subgraph Orders["Order Endpoints"]
            GET_ORDERS["GET /api/orders"]
            POST_ORDER["POST /api/orders"]
            GET_ORDER["GET /api/orders/:id"]
        end
    end
    Auth --> |"auth required: no"| PUBLIC((Public))
    Users --> |"auth required: yes"| PROTECTED((Protected))
    Products --> |"auth required: varies"| MIXED((Mixed))
    Orders --> |"auth required: yes"| PROTECTED`;
}

function generateComponentDiagram(data) {
  return `graph TB
    subgraph UI["Frontend Application"]
        subgraph Pages["Pages"]
            HOME[Home Page]
            LOGIN[Login Page]
            DASHBOARD[Dashboard Page]
            PRODUCTS[Products Page]
            ORDERS[Orders Page]
            PROFILE[Profile Page]
        end
        subgraph Components["Shared Components"]
            NAV[Navbar]
            FOOTER[Footer]
            TABLE[DataTable]
            FORM[FormBuilder]
            MODAL[Modal]
            CHART[Chart]
        end
        subgraph State["State Management"]
            STORE[Global Store]
            AUTH_STORE[Auth Store]
            API_STORE[API Store]
        end
        subgraph Services["Services"]
            API_SVC[API Service]
            AUTH_SVC[Auth Service]
            CACHE_SVC[Cache Service]
        end
    end
    Pages --> Components
    Pages --> State
    Components --> Services
    State --> Services
    Services --> |HTTP| API((Backend API))`;
}

function generateSequenceDiagram(data) {
  return `sequenceDiagram
    participant U as User
    participant FE as Frontend
    participant API as API Gateway
    participant AUTH as Auth Service
    participant SVC as Business Service
    participant DB as Database
    participant EXT as External API

    U->>FE: Click "Create Order"
    FE->>API: POST /api/orders
    API->>AUTH: Validate Token
    AUTH-->>API: Token Valid
    API->>SVC: Create Order
    SVC->>DB: Insert Order
    SVC->>EXT: Process Payment
    EXT-->>SVC: Payment Confirmed
    SVC->>DB: Update Order Status
    DB-->>SVC: Order Updated
    SVC-->>API: Order Created
    API-->>FE: 201 Created
    FE-->>U: Display Success`;
}

function generateDeployment(data) {
  return `graph TB
    subgraph Dev["Development"]
        DEV_ENV[Local Machine]
        DKR_COMPOSE[Docker Compose]
    end
    subgraph CI["CI/CD Pipeline"]
        GIT[Git Push]
        GH_ACTIONS[GitHub Actions]
        BUILD[Build & Test]
        LINT[Lint & TypeCheck]
        DOCKER_BUILD[Docker Build]
        PUSH_REG[Push to Registry]
    end
    subgraph Staging["Staging"]
        STG_K8S[Staging K8s]
        STG_DB[Staging DB]
        SMOKE[Smoke Tests]
    end
    subgraph Prod["Production"]
        PROD_LB[Load Balancer]
        PROD_K8S[Production K8s]
        PROD_DB[Production DB]
        MONITOR[Monitoring]
    end
    DEV_ENV --> GIT
    GIT --> GH_ACTIONS
    GH_ACTIONS --> BUILD
    BUILD --> LINT
    LINT --> DOCKER_BUILD
    DOCKER_BUILD --> PUSH_REG
    PUSH_REG --> STG_K8S
    STG_K8S --> SMOKE
    SMOKE --> PROD_LB
    PROD_LB --> PROD_K8S
    PROD_K8S --> MONITOR`;
}

function generateSecurityArchitecture(data) {
  return `graph TB
    subgraph External["External"]
        USER[User]
        ATTACKER[Potential Attacker]
    end
    subgraph Edge["Edge Protection"]
        WAF[WAF / CloudFlare]
        RATE[Rate Limiter]
        DDoS[DDoS Protection]
    end
    subgraph Application["Application Security"]
        AUTH[Auth: JWT / OAuth2]
        RBAC[Role Based Access Control]
        VALID[Input Validation]
        CORS[CORS Policy]
        CSP[Content Security Policy]
        ENCRYPT[Encryption at Rest]
        TLS[TLS 1.3 in Transit]
    end
    subgraph Secrets["Secrets Management"]
        VAULT[Secrets Vault]
        ENV[Environment Variables]
    end
    subgraph Audit["Audit & Compliance"]
        AUDIT[Audit Logging]
        LOGS[Access Logs]
        COMPLY[Compliance Checks]
    end
    USER --> WAF
    ATTACKER --> WAF
    WAF --> RATE
    RATE --> DDoS
    DDoS --> AUTH
    AUTH --> RBAC
    RBAC --> VALID
    VALID --> CORS
    CORS --> TLS
    TLS --> ENCRYPT
    ENCRYPT --> AUDIT
    VAULT --> ENV
    ENV --> AUTH
    AUDIT --> LOGS
    LOGS --> COMPLY`;
}

function generateIntegrationMap(data) {
  return `graph LR
    subgraph Internal["Our System"]
        API[API Layer]
        WK[Workers]
        SCH[Schedule Jobs]
    end
    subgraph ExternalIntegrations["External Integrations"]
        PGTO[Payment Gateway]
        EMAIL[Email Service]
        SMS[SMS Provider]
        S3[Object Storage]
        CDN[CDN]
        ANALYTICS[Analytics]
        MCP[MCP Servers]
    end
    API --> PGTO
    API --> EMAIL
    API --> SMS
    API --> MCP
    WK --> S3
    WK --> CDN
    WK --> ANALYTICS
    SCH --> EMAIL
    SCH --> SMS
    PGTO -.-> |webhook| API`;
}

function generateImprovementRoadmap(data) {
  return `gantt
    title Improvement Roadmap
    dateFormat YYYY-MM-DD
    axisFormat %b %Y
    
    section Critical
    Fix Security Vulnerabilities    :crit, 2025-01-01, 30d
    Database Index Optimization     :crit, 2025-01-15, 20d
    
    section High
    API Documentation               :2025-02-01, 45d
    Test Coverage Increase          :2025-02-15, 60d
    Error Handling Standardization  :2025-03-01, 30d
    
    section Medium
    CI/CD Pipeline Improvement      :2025-03-15, 45d
    Monitoring Dashboard            :2025-04-01, 30d
    Performance Optimization        :2025-04-15, 45d
    
    section Low
    Developer Onboarding Guide      :2025-05-01, 30d
    Code Comments & Docs            :2025-05-15, 45d
    Tech Debt Refactoring           :after docs, 60d`;
}

function generateProjectMindmap(data) {
  return `mindmap
  root((Project Map))
    Infrastructure
      Containers
      Orchestration
      Networking
      Storage
    Data Layer
      MongoDB
        Collections
        Indexes
      ChromaDB
        Embeddings
        Collections
    Backend
      API Routes
      Services
      Middleware
      Auth
    Frontend
      Pages
      Components
      State
      Services
    Business
      Domain Models
      Business Rules
      Workflows
    Integrations
      External APIs
      MCP Servers
      Webhooks
    Security
      AuthN / AuthZ
      Encryption
      Audit
    DevOps
      CI/CD
      Docker
      Deploy
    Observability
      Logging
      Monitoring
      Tracing
    Governance
      Docs
      ADRs
      Standards`;
}

main();
