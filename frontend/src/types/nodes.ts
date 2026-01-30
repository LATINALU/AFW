export type NodeType = 'prompt' | 'agent_l1' | 'agent_l2' | 'agent_l3' | 'agent_l4' | 'agent_l5' | 'ai_provider' | 'output_base' | 'output_final';

export interface NodeData {
  label: string;
  type: NodeType;
  agentName?: string;
  agentLevel?: number;
  additionalInstructions?: string;
  positivePrompt?: string;
  negativePrompt?: string;
  provider?: string;
  model?: string;
  temperature?: number;
  maxTokens?: number;
  result?: string;
}

export interface WorkflowNode {
  id: string;
  type: string;
  position: { x: number; y: number };
  data: NodeData;
}

export interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
  sourceHandle?: string;
  targetHandle?: string;
}

export interface Workflow {
  id: string;
  name: string;
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
  createdAt: Date;
  updatedAt: Date;
}
