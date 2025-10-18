# S2-Comprehensive Discovery: Kubernetes Technical Deep Dive

**Date**: October 17, 2025
**Research Method**: Technical specification review, architecture analysis
**Time Investment**: ~2 hours
**Confidence Level**: 90% (detailed technical review)

## Executive Summary

Kubernetes provides a comprehensive, well-architected API for container orchestration with strong backward compatibility guarantees for GA (stable) APIs. The system is built on extensible interfaces (CRI, CNI, CSI) that enable vendor choice within the ecosystem. However, **true portability requires understanding the boundaries**: while core workload APIs (Pods, Deployments) are 100% portable, infrastructure integrations (networking, storage, load balancing) are cloud-specific, creating 60-70% effective portability across environments.

---

## 1. Kubernetes Architecture Overview

### Control Plane Components

**kube-apiserver**:
- Central management entity, exposes Kubernetes API (REST/HTTP)
- Validates and processes API requests
- Stores state in etcd (distributed key-value store)
- Scales horizontally (multiple API server replicas for HA)

**etcd**:
- Distributed key-value store for cluster state
- Source of truth for all cluster data
- Consistent (CP in CAP theorem), uses Raft consensus
- Backup/restore etcd = backup/restore entire cluster

**kube-scheduler**:
- Assigns Pods to Nodes based on constraints
- Considers resource requirements, affinity/anti-affinity, taints/tolerations
- Extensible (custom schedulers supported)

**kube-controller-manager**:
- Runs controller loops (Deployment controller, ReplicaSet controller, etc.)
- Reconciles desired state (manifests) with actual state (running Pods)
- Implements Kubernetes' core automation (self-healing, scaling)

**cloud-controller-manager** (optional, cloud-specific):
- Integrates with cloud provider APIs (AWS, Azure, GCP)
- Manages LoadBalancer Services, Node lifecycle, Volume provisioning
- **Source of cloud portability challenges**

---

### Node Components

**kubelet**:
- Agent running on every Node
- Receives Pod specifications from API server
- Manages container lifecycle via CRI (Container Runtime Interface)
- Reports Node and Pod status back to API server
- Runs health checks (liveness, readiness, startup probes)

**kube-proxy**:
- Network proxy on every Node
- Implements Service abstraction (load balancing to Pods)
- Modes: iptables (default, O(n) performance), IPVS (O(1), better for large clusters)
- Configures kernel networking rules (NAT, routing)

**Container Runtime** (containerd, CRI-O, Docker via cri-dockerd):
- Actually runs containers (pulls images, starts processes)
- Implements CRI (Container Runtime Interface) to talk to kubelet
- OCI-compliant (uses runc, crun, or other OCI runtimes under the hood)

---

## 2. Core API Resources (Workloads)

### Pods

**Definition**: Smallest deployable unit, one or more containers with shared network and storage

**Lifecycle Phases**:
- **Pending**: Accepted by cluster, waiting for scheduling/image pull
- **Running**: Bound to Node, at least one container running
- **Succeeded**: All containers terminated successfully (exit 0)
- **Failed**: All containers terminated, at least one failed (non-zero exit)
- **Unknown**: Pod state can't be determined (Node communication failure)

**Init Containers** (run before app containers):
```yaml
spec:
  initContainers:
  - name: init-db
    image: busybox
    command: ['sh', '-c', 'until nslookup db; do sleep 1; done']
```

**Resource Requests & Limits**:
```yaml
resources:
  requests:
    memory: "64Mi"
    cpu: "250m"      # 0.25 CPU cores
  limits:
    memory: "128Mi"
    cpu: "500m"      # 0.5 CPU cores
```

- **Requests**: Guaranteed resources (scheduler considers when placing Pod)
- **Limits**: Maximum resources (Pod killed if exceeded - OOMKilled for memory)

**Quality of Service (QoS) Classes**:
- **Guaranteed**: All containers have requests = limits
- **Burstable**: At least one container has requests < limits
- **BestEffort**: No requests or limits set (evicted first under pressure)

---

### Deployments

**Purpose**: Manage stateless applications with rolling updates, scaling, rollbacks

**Key Features**:
- **Declarative updates**: Change image tag → automatic rollout
- **Rollback**: `kubectl rollout undo deployment/myapp`
- **Pausing/resuming**: Test changes before full rollout
- **Revision history**: Keep last N ReplicaSets for rollback

**Example Deployment**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1    # Max Pods down during update
      maxSurge: 1          # Max extra Pods during update
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
```

**Rolling Update Process**:
1. Create new ReplicaSet with updated Pod template
2. Scale up new ReplicaSet by maxSurge
3. Scale down old ReplicaSet by maxUnavailable
4. Repeat until new ReplicaSet has all replicas
5. Old ReplicaSet scaled to 0 (kept for rollback)

**Portability**: ✅ 100% portable (Deployments work identically across all Kubernetes clusters)

---

### StatefulSets

**Purpose**: Manage stateful applications (databases, queues) with stable identities

**Differences from Deployments**:
- **Stable network identities**: Pods get predictable DNS names (myapp-0, myapp-1, myapp-2)
- **Stable persistent storage**: Each Pod gets own PersistentVolumeClaim
- **Ordered deployment**: Pods created sequentially (0 → 1 → 2)
- **Ordered termination**: Pods deleted in reverse order (2 → 1 → 0)

**Use Cases**:
- **Databases**: MySQL, PostgreSQL, MongoDB (each Pod needs own data volume)
- **Message queues**: Kafka, RabbitMQ (partition/queue assignment based on Pod identity)
- **Distributed systems**: Elasticsearch, Cassandra (cluster membership based on identity)

**Portability**: ✅ Core concept portable, ⚠️ storage backend cloud-specific

---

### Services

**Purpose**: Expose Pods via stable DNS name and load balancing

**Service Types**:

1. **ClusterIP** (default): Internal-only, accessible within cluster
   ```yaml
   type: ClusterIP
   ```
   - DNS: `myservice.mynamespace.svc.cluster.local`
   - **Portability**: ✅ 100% portable

2. **NodePort**: Exposes Service on each Node's IP at static port
   ```yaml
   type: NodePort
   ports:
   - port: 80
     targetPort: 8080
     nodePort: 30080    # 30000-32767 range
   ```
   - Access: `<NodeIP>:30080`
   - **Portability**: ✅ 100% portable

3. **LoadBalancer**: Provisions cloud load balancer (AWS ELB, Azure LB, GCP LB)
   ```yaml
   type: LoadBalancer
   ```
   - **Portability**: ❌ Cloud-specific (annotations, behavior differ)
   - **AWS**: Creates Classic or Network Load Balancer
   - **Azure**: Creates Azure Load Balancer
   - **GCP**: Creates Google Cloud Load Balancer
   - **Migration**: Must reconfigure annotations, DNS, IP addresses

4. **ExternalName**: Maps Service to external DNS name
   ```yaml
   type: ExternalName
   externalName: api.example.com
   ```
   - **Portability**: ✅ 100% portable

---

## 3. Networking Deep Dive

### Pod-to-Pod Networking (CNI)

**Kubernetes Networking Requirements**:
- Every Pod gets unique IP address
- Pods can communicate with all other Pods without NAT
- Nodes can communicate with all Pods without NAT
- Pod's IP is the same as others see it (no NAT/masquerading)

**CNI Plugin Responsibility**:
1. Assign IP address to Pod
2. Create network interface in Pod's namespace (veth pair)
3. Configure routes on Node for Pod's IP
4. Ensure Pod can reach other Pods/Nodes

**Popular CNI Plugins**:

| Plugin | Approach | Performance | Features | Cloud Portability |
|--------|----------|-------------|----------|-------------------|
| **Calico** | Layer 3 (BGP routing) | High | NetworkPolicies, encryption | ✅ Portable |
| **Flannel** | Overlay (VXLAN) | Medium | Simple, beginner-friendly | ✅ Portable |
| **Cilium** | eBPF | Very High | Advanced policies, observability | ✅ Portable |
| **Weave Net** | Overlay (VXLAN) | Medium | Encryption, multicast | ✅ Portable |
| **AWS VPC CNI** | Native VPC | High | AWS VPC integration | ❌ AWS-only |
| **Azure CNI** | Native VNet | High | Azure VNet integration | ❌ Azure-only |

**Portability**: ✅ Open-source CNIs (Calico, Flannel) are portable. ❌ Cloud-native CNIs lock you to that cloud.

---

### Service Networking (kube-proxy)

**How kube-proxy Works**:

1. **Watch API server**: Monitor Service and Endpoint objects
2. **Configure routing**: Update iptables/IPVS rules on Node
3. **Load balance**: Distribute traffic across Pod IPs

**iptables Mode** (default):
- Creates DNAT rules: Service IP → random Pod IP
- Sequential rule evaluation (O(n) complexity)
- No configurable load-balancing algorithm (random selection)
- Scales to ~1,000 Services per cluster

**IPVS Mode** (production recommended for large clusters):
- Uses IPVS kernel module (designed for load balancing)
- Hash table lookup (O(1) complexity)
- Multiple algorithms: round-robin, least-connection, source-hash
- Scales to 10,000+ Services per cluster

**Service Discovery** (CoreDNS):
- Every Service gets DNS entry: `myservice.mynamespace.svc.cluster.local`
- Pods automatically configured with cluster DNS
- External DNS integration for Services with external IPs

**Portability**: ✅ kube-proxy internals are portable (all clusters use iptables/IPVS). ❌ LoadBalancer Services depend on cloud provider.

---

### NetworkPolicies (Firewall Rules)

**Purpose**: Control Pod-to-Pod and Pod-to-external traffic

**Example NetworkPolicy** (deny all ingress by default):
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
spec:
  podSelector: {}        # Apply to all Pods in namespace
  policyTypes:
  - Ingress
```

**Example NetworkPolicy** (allow frontend → backend):
```yaml
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

**CNI Support**:
- **Calico, Cilium, Weave Net**: Full NetworkPolicy support
- **Flannel**: No NetworkPolicy support (requires Canal or Calico overlay)
- **AWS VPC CNI, Azure CNI**: Partial support (depends on version)

**Portability**: ⚠️ NetworkPolicy spec is portable, but enforcement depends on CNI plugin.

---

## 4. Storage Deep Dive

### PersistentVolumes & PersistentVolumeClaims

**Architecture**:

1. **PersistentVolume (PV)**: Cluster-level resource representing storage (admin-provisioned or dynamic)
2. **PersistentVolumeClaim (PVC)**: Namespace-scoped request for storage (user-created)
3. **Binding**: Kubernetes matches PVC to suitable PV (size, access mode, StorageClass)

**Access Modes**:
- **ReadWriteOnce (RWO)**: Single Node, read-write (most cloud disks - EBS, Azure Disk, GCE PD)
- **ReadOnlyMany (ROX)**: Multiple Nodes, read-only (NFS)
- **ReadWriteMany (RWX)**: Multiple Nodes, read-write (NFS, CephFS, Azure Files, EFS)

**Lifecycle**:
- **Available**: PV is free, not yet bound to PVC
- **Bound**: PV is bound to PVC
- **Released**: PVC deleted, but PV not yet reclaimed
- **Failed**: Automatic reclamation failed

**Reclaim Policies**:
- **Retain**: PV remains after PVC deletion (manual cleanup required)
- **Delete**: PV and underlying storage deleted when PVC deleted (cloud disks)
- **Recycle** (deprecated): Data deleted, PV made available for new claims

---

### StorageClasses (Dynamic Provisioning)

**Purpose**: Define storage "tiers" (SSD, HDD, regional, multi-zone) with auto-provisioning

**Example StorageClass** (AWS EBS):
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "3000"
  encrypted: "true"
volumeBindingMode: WaitForFirstConsumer  # Provision in Pod's zone
```

**Example PVC** (requests fast-ssd):
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mydata
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: fast-ssd
  resources:
    requests:
      storage: 100Gi
```

**Dynamic Provisioning Flow**:
1. User creates PVC with `storageClassName: fast-ssd`
2. Kubernetes calls CSI driver for `fast-ssd` StorageClass
3. CSI driver provisions cloud disk (AWS EBS gp3, 100Gi)
4. CSI driver creates PV representing the disk
5. Kubernetes binds PVC to PV
6. Pod mounts PVC as volume

**Cloud-Specific StorageClasses**:
- **AWS**: `gp3` (SSD), `io2` (high IOPS), `st1` (HDD), `efs` (shared)
- **Azure**: `managed-premium` (SSD), `azurefile` (shared)
- **GCP**: `pd-ssd`, `pd-balanced`, `filestore` (shared)

**Portability**: ❌ StorageClasses are cloud-specific. Migration requires data backup/restore (Velero).

---

### CSI (Container Storage Interface)

**Pre-CSI** (in-tree plugins, deprecated):
- Kubernetes core contained cloud-specific code (AWS EBS, GCE PD, Azure Disk)
- Adding new storage required modifying Kubernetes source code
- Tightly coupled to Kubernetes release cycle

**Post-CSI** (out-of-tree plugins, current):
- Storage vendors implement CSI driver (separate project)
- Kubernetes core is storage-agnostic (no cloud-specific code)
- CSI drivers developed/released independently

**Major CSI Drivers**:
- **AWS EBS CSI**, **Azure Disk CSI**, **GCE PD CSI**: Cloud block storage
- **AWS EFS CSI**, **Azure Files CSI**, **GCP Filestore CSI**: Cloud file storage
- **Rook-Ceph**: Open-source distributed storage (portable)
- **Portworx**: Commercial multi-cloud storage

**Portability**: ✅ CSI standard is portable. ❌ Cloud-specific CSI drivers lock you to that cloud.

---

## 5. Security: RBAC (Role-Based Access Control)

### Core Concepts

**Subjects** (who):
- **Users**: External identity (not managed by Kubernetes)
- **ServiceAccounts**: Kubernetes-managed identity for Pods
- **Groups**: Collections of users/ServiceAccounts

**Resources** (what):
- Pods, Services, Deployments, Secrets, etc.

**Verbs** (actions):
- `get`, `list`, `watch`, `create`, `update`, `patch`, `delete`, `deletecollection`

---

### Roles & RoleBindings (Namespace-Scoped)

**Example Role** (read Pods/Services in namespace):
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: production
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list", "watch"]
```

**Example RoleBinding** (grant pod-reader to user jane):
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: production
  name: jane-pod-reader
subjects:
- kind: User
  name: jane
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

---

### ClusterRoles & ClusterRoleBindings (Cluster-Scoped)

**ClusterRole** (cluster-wide resources or non-namespaced resources):
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: node-reader
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "list", "watch"]
```

**ClusterRoleBinding** (grant cluster-wide access):
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: jane-node-reader
subjects:
- kind: User
  name: jane
roleRef:
  kind: ClusterRole
  name: node-reader
```

---

### Security Best Practices

**1. Principle of Least Privilege**:
- Grant minimum permissions required
- Use Roles (namespace-scoped) over ClusterRoles when possible

**2. Avoid cluster-admin**:
- `cluster-admin` ClusterRole has unrestricted access
- Create custom Roles with specific permissions instead

**3. Avoid system:masters Group**:
- Bypasses all RBAC checks (cannot be revoked)
- Never add users to this group

**4. Watch for Privilege Escalation Verbs**:
- `escalate`: Can modify Roles to grant higher privileges
- `bind`: Can bind higher-privileged Roles to subjects
- `create` on PersistentVolumes: Can mount host filesystem
- `create` on Pods: Can run privileged containers

**5. Avoid Wildcards** (`*`):
- `resources: ["*"]` grants access to all resources, including future ones
- `verbs: ["*"]` grants all actions, including dangerous ones

**6. ServiceAccount Security**:
- Create application-specific ServiceAccounts (not default)
- Set `automountServiceAccountToken: false` to prevent auto-mounting

**Portability**: ✅ RBAC specs are portable. ❌ Cloud IAM integration (IRSA, AAD, Workload Identity) is cloud-specific.

---

## 6. Autoscaling

### Horizontal Pod Autoscaler (HPA)

**Purpose**: Scale number of Pods based on metrics (CPU, memory, custom metrics)

**Example HPA** (scale based on CPU):
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70    # Target 70% CPU
```

**How HPA Works**:
1. HPA controller queries Metrics Server every 15 seconds (default)
2. Calculates desired replicas: `ceil[currentReplicas * (currentMetric / targetMetric)]`
3. Adjusts Deployment replicas (scales up/down)
4. Waits cooldown period before scaling again (3 min scale-up, 5 min scale-down)

**Metrics Types**:
- **Resource metrics**: CPU, memory (via Metrics Server)
- **Custom metrics**: Application metrics (via Prometheus Adapter)
- **External metrics**: Cloud metrics (via cloud provider adapters)

**Portability**: ✅ HPA spec portable. ⚠️ Custom/external metrics require additional components (Prometheus, cloud adapters).

---

### Vertical Pod Autoscaler (VPA)

**Purpose**: Adjust CPU/memory requests/limits for Pods based on actual usage

**Components**:
- **Recommender**: Analyzes historical usage, provides recommendations
- **Updater**: Evicts Pods to apply recommendations (rolling restart)
- **Admission Plugin**: Applies recommendations on Pod creation

**VPA Modes**:
- **Off**: Recommendations only (no automatic updates)
- **Initial**: Apply recommendations on Pod creation only
- **Recreate**: Evict Pods to apply recommendations (rolling restart)
- **Auto**: Future mode (in-place updates without restart - not yet available)

**Example VPA**:
```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: myapp-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  updatePolicy:
    updateMode: "Recreate"
```

**HPA vs VPA**:
- **HPA**: Scales horizontally (more Pods)
- **VPA**: Scales vertically (bigger Pods)
- **Cannot** use HPA and VPA on same metric (creates conflict)
- **Can** use HPA (CPU) + VPA (memory) on different metrics

**Portability**: ✅ VPA is portable (separate component, not Kubernetes core).

---

### Cluster Autoscaler

**Purpose**: Add/remove Nodes based on Pod scheduling demand

**How It Works**:
1. Monitors Pods in **Pending** state (unschedulable due to insufficient resources)
2. If Pending Pods exist, adds Node to cluster (via cloud provider API)
3. If Nodes are underutilized (low resource usage), removes Nodes
4. Respects PodDisruptionBudgets, critical Pods, and drain timeouts

**Cloud Provider Integration**:
- **AWS**: Calls Auto Scaling Groups (ASG) to add/remove EC2 instances
- **Azure**: Calls Virtual Machine Scale Sets (VMSS)
- **GCP**: Calls Managed Instance Groups (MIG)

**Portability**: ❌ Cluster Autoscaler is cloud-specific (requires cloud provider API integration).

---

## 7. Ingress & API Gateway

### Ingress

**Purpose**: HTTP/HTTPS routing (map URLs to Services)

**Example Ingress**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp
            port:
              number: 80
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
```

**Ingress Controllers** (not part of Kubernetes core):
- **NGINX Ingress Controller** (most popular, open-source)
- **Traefik** (modern, dynamic config)
- **HAProxy Ingress**
- **Contour** (Envoy-based, CNCF project)
- **AWS ALB Ingress Controller** (AWS-specific)
- **Azure Application Gateway Ingress Controller** (Azure-specific)

**Portability**: ✅ Ingress spec portable. ⚠️ Controller-specific annotations not portable (must rewrite for different controllers).

---

## 8. API Versioning & Stability

### Deprecation Policy

**GA (Stable) APIs**:
- Remain available for all future releases within major version
- No breaking changes allowed
- Example: `apps/v1` Deployment (stable since 1.9, still supported in 1.30)

**Beta APIs**:
- Max lifetime: 9 months or 3 releases (whichever longer)
- Deprecation notice: 9 months or 3 releases before removal
- Example: HPA `autoscaling/v2beta2` (deprecated 1.23, removed 1.26)

**Alpha APIs**:
- Disabled by default
- Can be removed at any time without notice

**Upgrade Safety**: Kubernetes ensures smooth upgrades (n-1 version compatibility). Example: If using 1.28 APIs, can upgrade to 1.29 safely.

**Portability**: ✅ GA APIs provide excellent portability across Kubernetes versions.

---

## Summary: Technical Portability Matrix

| Component | Portability | Notes |
|-----------|-------------|-------|
| **Pods** | ✅ 100% | Fully portable |
| **Deployments** | ✅ 100% | Fully portable |
| **StatefulSets** | ✅ 95% | Portable, storage backend cloud-specific |
| **Services (ClusterIP, NodePort)** | ✅ 100% | Fully portable |
| **Services (LoadBalancer)** | ❌ 30% | Cloud-specific annotations, IPs |
| **Ingress** | ⚠️ 70% | Spec portable, annotations controller-specific |
| **PersistentVolumes** | ❌ 40% | Cloud-specific storage backends |
| **StorageClasses** | ❌ 20% | Cloud-specific provisioners |
| **NetworkPolicies** | ⚠️ 80% | Spec portable, enforcement CNI-specific |
| **RBAC** | ✅ 95% | Portable, cloud IAM integration differs |
| **HPA** | ✅ 90% | Portable, custom metrics require setup |
| **VPA** | ✅ 90% | Portable (separate component) |
| **Cluster Autoscaler** | ❌ 0% | Cloud-specific (AWS ASG, Azure VMSS, GCP MIG) |

**Overall Portability: 60-70%** (core workloads portable, infrastructure integrations cloud-specific)

---

**Next**: S3-Need-Driven (Use Cases, Migrations), S4-Strategic (Long-Term Viability)
