import jsonpickle
from langgraph.typing import InputT
from langgraph.types import RunnableConfig, StreamMode, All, Sequence, Any

import httpx
from typing import Any, AsyncIterator, Iterator, Sequence

from examples.agents.create_simple_agent import response


class RemoteAgent:
    def __init__(self, path: str):
        self.base_url = path.rstrip("/")
        self.http_client_sync = httpx.Client(timeout=360)
        self.http_client_async = httpx.AsyncClient(timeout=360)

        self.info = self.info()
        self.name = self.info.get("name")
        self.description = self.info.get("description")
        self.skills = self.info.get("skills")
        self.tools = []

    def _request_sync(self, path: str = "", **kwargs: Any) -> Any:
        print(5*"*********** start *************+\n")
        dict_con_objetos = kwargs.get("json", {})
        print(f"Requesting {self.base_url}/{path} with objects: {dict_con_objetos}")
        
        data_pickled_string = jsonpickle.encode(dict_con_objetos, unpicklable=False)
        
        print(5*"*********** end *************+\n")
        
        response = self.http_client_sync.post(f"{self.base_url}/{path}", content=data_pickled_string)
        response.raise_for_status()
        return jsonpickle.decode(response.json())

    async def _request_async(self, path: str = "", **kwargs: Any) -> Any:
        print(5*"*********** start *************+\n")
        dict_con_objetos = kwargs.get("json", {})
        print(f"Requesting {self.base_url}/{path} with objects: {dict_con_objetos}")
        
        data_pickled_string = jsonpickle.encode(dict_con_objetos, unpicklable=False)
        
        print(5*"*********** end *************+\n")

        response = await self.http_client_async.post(
            f"{self.base_url}/{path}",
            content=data_pickled_string,
            headers={"Content-Type": "application/json"} # Buena práctica
        )

        response.raise_for_status()
        
        # 4. Decodifica la respuesta del servidor, que también viene con jsonpickle
        return jsonpickle.decode(response.text)

    def invoke(
        self,
        input: InputT,
        config: RunnableConfig | None = None,
        *,
        stream_mode: StreamMode = "values",
        print_mode: StreamMode | Sequence[StreamMode] = (),
        output_keys: str | Sequence[str] | None = None,
        interrupt_before: All | Sequence[str] | None = None,
        interrupt_after: All | Sequence[str] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | Any:
        return self._request_sync(
            path="invoke",
            json={
                "input": input,
                "config": config,
                "stream_mode": stream_mode,
                "print_mode": print_mode,
                "output_keys": output_keys,
                "interrupt_before": interrupt_before,
                "interrupt_after": interrupt_after,
                **kwargs,
            },
        )

    async def ainvoke(
        self,
        input: InputT,
        config: RunnableConfig | None = None,
        *,
        stream_mode: StreamMode = "values",
        print_mode: StreamMode | Sequence[StreamMode] = (),
        output_keys: str | Sequence[str] | None = None,
        interrupt_before: All | Sequence[str] | None = None,
        interrupt_after: All | Sequence[str] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | Any:
        return await self._request_async(
            path="ainvoke",
            json={
                "input": input,
                "config": config,
                "stream_mode": stream_mode,
                "print_mode": print_mode,
                "output_keys": output_keys,
                "interrupt_before": interrupt_before,
                "interrupt_after": interrupt_after,
                **kwargs,
            },
        )

    def stream(
        self,
        input: InputT,
        config: RunnableConfig | None = None,
        *,
        stream_mode: StreamMode | Sequence[StreamMode] | None = None,
        print_mode: StreamMode | Sequence[StreamMode] = (),
        output_keys: str | Sequence[str] | None = None,
        interrupt_before: All | Sequence[str] | None = None,
        interrupt_after: All | Sequence[str] | None = None,
        checkpoint_during: bool | None = None,
        debug: bool | None = None,
        subgraphs: bool = False,
    ) -> Iterator[dict[str, Any] | Any]:
        payload = {
            "input": input,
            "config": config,
            "stream_mode": stream_mode,
            "print_mode": print_mode,
            "output_keys": output_keys,
            "interrupt_before": interrupt_before,
            "interrupt_after": interrupt_after,
            "checkpoint_during": checkpoint_during,
            "debug": debug,
            "subgraphs": subgraphs,
        }
        with self.http_client_sync.stream(
            "POST", f"{self.base_url}/stream", json=payload
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    try:
                        yield jsonpickle.decode(line)
                    except Exception as e:
                        print(f"Error decoding stream chunk: {e}")

    async def astream(
        self,
        input: InputT,
        config: RunnableConfig | None = None,
        *,
        stream_mode: StreamMode | Sequence[StreamMode] | None = None,
        print_mode: StreamMode | Sequence[StreamMode] = (),
        output_keys: str | Sequence[str] | None = None,
        interrupt_before: All | Sequence[str] | None = None,
        interrupt_after: All | Sequence[str] | None = None,
        checkpoint_during: bool | None = None,
        debug: bool | None = None,
        subgraphs: bool = False,
    ) -> AsyncIterator[dict[str, Any] | Any]:
        payload = {
            "input": input,
            "config": config,
            "stream_mode": stream_mode,
            "print_mode": print_mode,
            "output_keys": output_keys,
            "interrupt_before": interrupt_before,
            "interrupt_after": interrupt_after,
            "checkpoint_during": checkpoint_during,
            "debug": debug,
            "subgraphs": subgraphs,
        }
        async with self.http_client_async.stream(
            "POST",
            f"{self.base_url}/astream",
            json=payload,
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line:
                    try:
                        yield jsonpickle.decode(line)
                    except Exception as e:
                        print(f"Error decoding async stream chunk: {e}")

    def info(self):
        response = self.http_client_sync.get(f"{self.base_url}/info")
        return response.json()
