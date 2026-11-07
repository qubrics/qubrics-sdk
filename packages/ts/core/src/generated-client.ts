import { authToken } from "./auth.js";
import { createErrorInterceptor } from "./errors.js";
import { createRetryingFetch } from "./retry.js";
import type {
  ApiKeyKind,
  GeneratedSendmuxClient,
  GeneratedSendmuxClientConfig,
  SendmuxClientConfig,
} from "./types.js";

const clientsWithErrorInterceptors = new WeakSet<object>();
const clientsWithRequestReplayInterceptors = new WeakSet<object>();
const clientReplayBodies = new WeakMap<object, WeakMap<Request, string>>();

export function configureGeneratedClient<TClient extends GeneratedSendmuxClient>(
  client: TClient,
  config: SendmuxClientConfig,
  apiKeyKind: ApiKeyKind,
): TClient {
  const env = (globalThis as { process?: { env?: Record<string, string | undefined> } }).process?.env ?? {};
  if (config.apiKey === undefined && config.accessToken === undefined) {
    const apiKey = env.QUBRICS_API_KEY || env.SENDMUX_API_KEY;
    const accessToken = env.QUBRICS_ACCESS_TOKEN || env.SENDMUX_ACCESS_TOKEN;
    config = { ...config, ...(apiKey ? { apiKey } : {}), ...(accessToken ? { accessToken } : {}) };
  }
  const replayBodies = replayBodyStoreFor(client);
  const bearerToken = authToken({ ...config, apiKeyKind });
  const nextConfig: GeneratedSendmuxClientConfig = {
    auth: (security?: { type: string; name?: string }) => {
      if (security?.type === "apiKey" &&
          (security.name === "X-Qubrics-Upload-Token" || security.name === "X-Sendmux-Upload-Token")) {
        return "";
      }
      return bearerToken();
    },
    fetch: createRetryingFetch(config.retry, config.fetch, replayBodies),
    throwOnError: true,
  };

  const baseUrl = config.baseUrl ?? (env.QUBRICS_BASE_URL || env.SENDMUX_BASE_URL);
  if (baseUrl) {
    nextConfig.baseUrl = baseUrl;
  }

  client.setConfig(nextConfig);

  if (!clientsWithRequestReplayInterceptors.has(client)) {
    client.interceptors.request.use((request, options) => {
      if (typeof options.serializedBody === "string") {
        replayBodies.set(request, options.serializedBody);
      }

      return request;
    });
    clientsWithRequestReplayInterceptors.add(client);
  }

  if (!clientsWithErrorInterceptors.has(client)) {
    client.interceptors.error.use(createErrorInterceptor());
    clientsWithErrorInterceptors.add(client);
  }

  return client;
}

function replayBodyStoreFor(client: object): WeakMap<Request, string> {
  const existing = clientReplayBodies.get(client);
  if (existing) {
    return existing;
  }

  const replayBodies = new WeakMap<Request, string>();
  clientReplayBodies.set(client, replayBodies);
  return replayBodies;
}
