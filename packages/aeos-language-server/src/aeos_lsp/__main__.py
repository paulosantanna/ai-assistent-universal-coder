from __future__ import annotations

import argparse
import logging
import os
import signal
import sys

from aeos_lsp.constants import (
    EXIT_SUCCESS,
    EXIT_INTERNAL_ERROR,
    EXIT_INVALID_CONFIG,
    SERVER_NAME,
    SERVER_VERSION,
)
from aeos_lsp.logging_config import setup_logging

logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="aeos-lsp",
        description=f"{SERVER_NAME} v{SERVER_VERSION} - AEOS Language Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
modes:
  stdio         (default) LSP via stdin/stdout
  tcp           LSP via TCP socket
  validate      Validate workspace and exit
  index         Index workspace and exit
  diagnostics   Run diagnostics and output results
  doctor        Diagnose server configuration
  capabilities  Print server capabilities as JSON
  version       Print version and exit
        """,
    )

    parser.add_argument(
        "--stdio",
        action="store_true",
        help="Run LSP server over stdin/stdout (default)",
    )
    parser.add_argument(
        "--tcp",
        action="store_true",
        help="Run LSP server over TCP",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="TCP host address (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=2087,
        help="TCP port (default: 2087)",
    )
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["stdio", "tcp", "validate", "index", "diagnostics", "doctor", "capabilities", "version"],
        default=None,
        help="Server mode (default: stdio)",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=None,
        help="Workspace path for validate/index/diagnostics modes",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level (default: WARNING)",
    )
    parser.add_argument(
        "--log-file",
        type=str,
        default=None,
        help="Path to log file",
    )
    parser.add_argument(
        "--format",
        type=str,
        default="editor",
        choices=["editor", "json", "sarif", "agent"],
        dest="output_format",
        help="Output format for diagnostics mode (default: editor)",
    )

    args = parser.parse_args()

    resolved_mode: str = args.mode or "stdio"
    if args.stdio:
        resolved_mode = "stdio"
    elif args.tcp:
        resolved_mode = "tcp"

    setup_logging(level=args.log_level, log_file=args.log_file)
    logger.debug("aeos-lsp starting in %s mode", resolved_mode)

    _setup_signal_handlers()

    try:
        exit_code = _route_mode(resolved_mode, args)
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(EXIT_SUCCESS)
    except Exception:
        logger.exception("Fatal error in mode '%s'", resolved_mode)
        sys.exit(EXIT_INTERNAL_ERROR)


def _route_mode(mode: str, args: argparse.Namespace) -> int:
    if mode == "version":
        return _handle_version()
    elif mode == "capabilities":
        return _handle_capabilities()
    elif mode == "doctor":
        return _handle_doctor()
    elif mode == "validate":
        return _handle_validate(args)
    elif mode == "index":
        return _handle_index(args)
    elif mode == "diagnostics":
        return _handle_diagnostics(args)
    elif mode == "tcp":
        return _handle_tcp(args)
    else:
        return _handle_stdio(args)


def _handle_version() -> int:
    print(f"{SERVER_NAME} v{SERVER_VERSION}")
    return EXIT_SUCCESS


def _handle_capabilities() -> int:
    from aeos_lsp.cli import cli_capabilities
    return cli_capabilities()


def _handle_doctor() -> int:
    from aeos_lsp.cli import cli_doctor
    return cli_doctor()


def _handle_validate(args: argparse.Namespace) -> int:
    from aeos_lsp.cli import cli_validate
    path = args.path or os.getcwd()
    return cli_validate(path)


def _handle_index(args: argparse.Namespace) -> int:
    from aeos_lsp.cli import cli_index
    path = args.path or os.getcwd()
    return cli_index(path)


def _handle_diagnostics(args: argparse.Namespace) -> int:
    from aeos_lsp.cli import cli_diagnostics
    path = args.path or os.getcwd()
    return cli_diagnostics(path, args.output_format)


def _handle_tcp(args: argparse.Namespace) -> int:
    from aeos_lsp.server import AEOSLanguageServer
    from aeos_lsp.configuration import LSPClientConfig
    config = LSPClientConfig(log_level=args.log_level)
    server = AEOSLanguageServer(config=config)
    server.start_tcp(host=args.host, port=args.port)
    return EXIT_SUCCESS


def _handle_stdio(args: argparse.Namespace) -> int:
    from aeos_lsp.server import AEOSLanguageServer
    from aeos_lsp.configuration import LSPClientConfig
    config = LSPClientConfig(log_level=args.log_level)
    server = AEOSLanguageServer(config=config)
    server.start_stdio()
    return EXIT_SUCCESS


def _setup_signal_handlers() -> None:
    try:

        def _sigint_handler(signum: int, frame: object) -> None:
            logger.info("Received SIGINT, shutting down")
            sys.exit(EXIT_SUCCESS)

        def _sigterm_handler(signum: int, frame: object) -> None:
            logger.info("Received SIGTERM, shutting down")
            sys.exit(EXIT_SUCCESS)

        signal.signal(signal.SIGINT, _sigint_handler)
        signal.signal(signal.SIGTERM, _sigterm_handler)
    except (ValueError, AttributeError):
        pass


if __name__ == "__main__":
    main()
