# Feature-of [GEN]: Aspect Graph Specification

This document defines a flexible, aspect-based specification system with a clear root node and a tree-shaped primary structure.

## Use Case: Core model as an aspect network [Spec]

### Story: Requirements are modeled as aspects with a clear tree backbone {specification, structure} [Spec]

#### Item: The specification uses aspects as the smallest business units with stable ID, title, text, status, labels, and optional metadata. [Spec]

#### Item: Relations between aspects are typed and available at least as `CONSISTS_OF`, `RELATED_TO`, `DEPENDS_ON`, `CONFLICTS_WITH`, and `DERIVES_FROM`. [Spec]

#### Item: The specification network has exactly one business root node as entry point for the primary structure. [Spec]

#### Item: `CONSISTS_OF` follows a hard integrity rule: the relation forms a tree (connected, acyclic, one parent per child except root). [Spec]

#### Item: Other relation types may allow cycles when they are documented and do not violate the `CONSISTS_OF` tree structure. [Spec]

## Use Case: Author-friendly editing in the web app [Spec]

### Story: Aspects can be created, linked, and navigated easily {view, panel, function} [Spec]

#### Item: The system provides a standalone web UI where aspects are edited as text, relations are created, and graph navigation is available. [Spec]

#### Item: Editing is text-centered and avoids technical hurdles for business users. [Spec]

#### Item: Backlinks (`linked from`) and relation-type filters are available for navigation. [Spec]

## Use Case: Large-scale graph exploration [Spec]

### Story: The full graph remains navigable at any practical scale {view, architecture, quality} [Spec]

#### Item: The web app provides a continuous graph canvas for pan and zoom navigation across the complete model view. [Spec]

#### Item: The graph canvas supports very deep zoom-in and zoom-out behavior with map-like interaction semantics. [Spec]

#### Item: The rendering model uses level-of-detail behavior so distant views aggregate information and near views reveal full node and edge detail. [Spec]

#### Item: The rendering model uses viewport-based virtualization and progressive loading so visible regions remain responsive even for very large graphs. [Spec]

#### Item: The system defines practical technical limits (for example precision, memory, and rendering budgets) and handles limit conditions gracefully instead of failing hard. [Spec]

## Use Case: Standalone operation and app integration [Spec]

### Story: The specification system is independently deployable and integrable {architecture, process} [Spec]

#### Item: The specification application is deployable as an independent product and is not bound to a single business app. [Spec]

#### Item: Integration into target apps is provided through stable interfaces (deep links, API, and optional SDK). [Spec]

#### Item: Target apps can reference aspects without taking over ownership of the business model. [Spec]

## Use Case: Linking specification and app artifacts [Spec]

### Story: Aspects explain concrete parts of target applications {documentation, function} [Spec]

#### Item: Aspects can reference app artifacts such as routes, UI components, API endpoints, data objects, test cases, or code symbols. [Spec]

#### Item: Artifact references are typed and bidirectional so that each app part is traceable to the aspects that justify it. [Spec]

#### Item: Changes in linked app artifacts mark affected aspects as review-required. [Spec]

## Use Case: Multi-format specification [Spec]

### Story: Additional specification formats are managed as first-class artifacts {data, architecture} [Spec]

#### Item: The system supports not only prose text but also attachments and content in formats such as PlantUML (`.puml`), YAML, JSON, and Markdown. [Spec]

#### Item: Format content can be assigned to aspects or relation groups and is versioned. [Spec]

#### Item: Preview or rendering capabilities are provided for supported formats where technically feasible. [Spec]

## Use Case: Ticketing as part of the aspect system [Spec]

### Story: Delivery work is managed through tickets linked to aspects {process, quality} [Spec]

#### Item: The system provides a ticketing mechanism with at least type, priority, ownership, status, and due-date information. [Spec]

#### Item: Every delivery ticket is linked to at least one aspect. [Spec]

#### Item: Ticket relations such as `IMPLEMENTS`, `VALIDATES`, and `BLOCKED_BY` are explicitly modelable. [Spec]

#### Item: Unlinked delivery tickets are treated as a governance violation. [Spec]

## Use Case: Pipeline from specification to acceptance [Spec]

### Story: Aspects move through a clear delivery flow {process, quality} [Spec]

#### Item: Aspects or aspect versions provide a controllable pipeline state with at least `SPEC`, `IMPLEMENT`, `TEST`, and `ACCEPT`. [Spec]

#### Item: Transition to `IMPLEMENT` requires links to implementation tickets. [Spec]

#### Item: Transition to `TEST` requires documented test activities or linked test tickets. [Spec]

#### Item: Transition to `ACCEPT` requires traceable business sign-off. [Spec]

## Use Case: Change management for aspects and relations [Spec]

### Story: Business and structural changes remain controllable {quality, data} [Spec]

#### Item: Aspects and relations are versioned; each change records reason, author, and timestamp. [Spec]

#### Item: Semantic text changes and structural changes (relation changes) are traceable separately. [Spec]

#### Item: Removing or detaching aspects with active references requires an explicit impact check. [Spec]

#### Item: Changes to `CONSISTS_OF` are persisted only if single-root and tree rules remain valid. [Spec]

#### Item: Upstream changes may invalidate prior acceptances and set affected nodes to `REVIEW_REQUIRED`. [Spec]

## Use Case: Incremental AI context delivery [Spec]

### Story: AI assistants receive only the relevant specification slice {architecture, quality} [Spec]

#### Item: For AI tasks, a context bundle is generated from seed aspects, dependent aspects, acceptance criteria, artifact references, and constraints. [Spec]

#### Item: Context delivery is incremental based on changes since a known bundle version, instead of full retransmission of the entire specification. [Spec]

#### Item: Aspect or relation changes emit delta events used for targeted re-indexing and bundle recomposition. [Spec]

#### Item: AI-generated outputs must reference affected aspect IDs to ensure traceability. [Spec]

## Use Case: Quality gates and governance [Spec]

### Story: Consistency is enforced through technical and process gates {quality, specification} [Spec]

#### Item: CI blocks on violations of `CONSISTS_OF` tree rules (multiple roots, cycles, multiple parents), dangling relations, invalid status values, and missing aspect references in delivery changes. [Spec]

#### Item: Every implementation change is mapped to at least one aspect and visible as evidence in review. [Spec]

#### Item: Reader views by domain, status, and relation type are part of the default output to preserve graph readability. [Spec]
