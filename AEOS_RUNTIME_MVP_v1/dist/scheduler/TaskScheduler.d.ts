import type { Task } from "../types.js";
export declare class TaskScheduler {
    createPlan(projectPath: string, objective: string): Task;
    listTasks(projectPath: string): Task[];
    readTask(projectPath: string, taskId: string): Task | null;
}
