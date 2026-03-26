# Project Runtime Surface Map

## How To Use This Map

- Add one row for each supported runtime surface.
- Link `Helper Or Bootstrap` to a reusable helper skill when the runtime loop is already supported.
- If the surface is already mapped but no reusable helper exists yet, add one narrow helper before replacing a temporary bootstrap link with the helper path.
- Link `Helper Or Bootstrap` to a bootstrap package when the repository still needs to define that surface.
- Copy the chosen runtime surface into `03-detailed-design.md`, record the executed path in `04-verification.md`, and list artifacts plus residual risks in `05-evidence.md`.

| Surface | Purpose | Prerequisites | Driver | Evidence | Helper Or Bootstrap |
| --- | --- | --- | --- | --- | --- |
| API | Validate request and response behavior against a running service | Local env, seed data, auth fixture | `uv run ...` or project API driver | responses, traces, logs | `skills/<project-api-runtime>/SKILL.md` |
| Browser | Validate end-user flows in a real browser | Running app, test account | browser helper command or script | screenshots, console logs, network traces | `docs/task-packages/<bootstrap-browser-runtime>/README.md` |
| Worker | Validate queue or background job behavior | Worker env, fixture input | worker runner or trigger script | logs, output records, metrics | `skills/<project-worker-runtime>/SKILL.md` |

## Notes

- Keep each helper skill bounded to one dominant runtime surface.
- If a surface cannot state prerequisites, evidence, or driver steps clearly, open a bootstrap package before treating it as reusable.
