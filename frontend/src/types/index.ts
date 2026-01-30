export interface Agent {
  name: string;
  displayName?: string;
  role: string;
  level: number;
  specialty?: string;
}

export interface AgentResponse {
  agent_id: string;
  agent_name: string;
  level: number;
  specialty: string;
  content: string;
  timestamp: Date;
}

export interface AgentDialogue {
  agentName: string;
  message: string;
  timestamp: Date;
}

export interface AgentProgress {
  agent_id: string;
  agent_name: string;
  level?: number;
  specialty?: string;
  status: "pending" | "processing" | "completed" | "error";
  progress?: number;
  current_step?: string;
  result?: string;
}

export interface Message {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: Date;
  agents?: string[];
  agentResponses?: AgentResponse[];
  status?: "pending" | "processing" | "completed" | "error";
  dialogues?: AgentDialogue[];
  agentProgress?: AgentProgress[];
  a2a_messages_count?: number;
  a2a_responses_count?: number;
}
