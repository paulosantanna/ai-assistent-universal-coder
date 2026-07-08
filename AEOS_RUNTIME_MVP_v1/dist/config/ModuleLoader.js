import { existsSync, readdirSync } from "node:fs";
import { join } from "node:path";
export class ModuleLoader {
    load(projectPath) {
        const aeosPath = join(projectPath, ".aeos");
        return {
            agentFileExists: existsSync(join(aeosPath, "AGENT.md")),
            foundationFiles: this.listMarkdown(join(aeosPath, "foundation")),
            executionFiles: this.listMarkdown(join(aeosPath, "execution")),
            reasoningFiles: this.listMarkdown(join(aeosPath, "reasoning")),
            knowledgeFiles: this.listMarkdown(join(aeosPath, "knowledge")),
            engineeringFiles: this.listMarkdown(join(aeosPath, "engineering")),
            verificationFiles: this.listMarkdown(join(aeosPath, "verification")),
            governanceFiles: this.listMarkdown(join(aeosPath, "governance")),
            operationsFiles: this.listMarkdown(join(aeosPath, "operations"))
        };
    }
    listMarkdown(dir) {
        if (!existsSync(dir))
            return [];
        return readdirSync(dir).filter((name) => name.toLowerCase().endsWith(".md")).sort();
    }
}
//# sourceMappingURL=ModuleLoader.js.map