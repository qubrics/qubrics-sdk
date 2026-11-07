import {
  configureGeneratedClient,
  type SurfaceClientConfig,
} from "@qubrics/core";

import {
  createClient,
  type Client,
} from "./generated/client/index.js";

export * from "./generated/sdk.gen.js";
export type { Client as SendingClient } from "./generated/client/index.js";

const DEFAULT_BASE_URL = "https://smtp.qubrics.com/api/v1";

export function createSendingClient(config: SurfaceClientConfig): Client {
  const client = createClient({ baseUrl: config.baseUrl ?? DEFAULT_BASE_URL });
  return configureGeneratedClient(client, config, "sending");
}

export const configureSending = createSendingClient;
