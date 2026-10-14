<!-- Package: 00_skills/(architecture)/tactical-ddd; relative command/resource examples resolve from that package or workspace root. -->

## Quick Anemia Signals (scan first)

```
public setX() / public setY()        → behaviour should be encapsulated
service.doX(entity, ...)              → logic likely belongs in entity
entity.setA(); entity.setB(); ...     → setter chain = missing intent method
no domain methods beyond getters      → pure data bag
```

---
