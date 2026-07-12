from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from lsprotocol.types import (
    WINDOW_WORK_DONE_PROGRESS_CANCEL,
    WorkDoneProgressBegin,
    WorkDoneProgressCancelParams,
    WorkDoneProgressReport,
    WorkDoneProgressEnd,
)

from aeos_lsp.protocol.progress import (
    ProgressManager,
    ProgressReporter,
    _handle_work_done_progress_cancel,
    register_progress_handlers,
)


@pytest.fixture
def mock_ls():
    ls = MagicMock()
    ls.progress = MagicMock()
    return ls


class TestProtocolProgress:
    def test_work_done_progress(self, mock_ls):
        mgr = ProgressManager(mock_ls)
        reporter = mgr.create(
            token="test-token",
            title="Test Progress",
        )
        assert reporter is not None
        assert reporter._title == "Test Progress"

    def test_progress_report(self, mock_ls):
        mgr = ProgressManager(mock_ls)
        reporter = mgr.create(
            token="report-token",
            title="Reporting",
        )
        reporter.begin(message="Starting", percentage=0)
        mock_ls.progress.begin.assert_called_once()
        reporter.report(message="In progress", percentage=50)
        mock_ls.progress.report.assert_called_once()
        args = mock_ls.progress.report.call_args[0]
        assert args[0] == "report-token"
        report_val = args[1]
        assert report_val.kind == "report"
        assert report_val.percentage == 50

    def test_progress_end(self, mock_ls):
        mgr = ProgressManager(mock_ls)
        reporter = mgr.create(
            token="end-token",
            title="Ending",
        )
        reporter.begin()
        reporter.end(message="Done")
        mock_ls.progress.end.assert_called_once()
        args = mock_ls.progress.end.call_args[0]
        end_val = args[1]
        assert end_val.kind == "end"
        assert end_val.message == "Done"

    def test_progress_cancel_handler(self):
        ls = MagicMock()
        params = WorkDoneProgressCancelParams(token="test")
        _handle_work_done_progress_cancel(ls, params)

    def test_progress_create_and_begin(self, mock_ls):
        mgr = ProgressManager(mock_ls)
        reporter = mgr.create_and_begin(
            token="auto",
            title="Auto Begin",
            message="Auto",
            percentage=10,
        )
        assert reporter is not None
        mock_ls.progress.begin.assert_called_once()

    def test_register_progress_handlers(self):
        ls = MagicMock()
        ls.protocol.fm.add_builtin_feature = MagicMock()
        register_progress_handlers(ls)
        ls.protocol.fm.add_builtin_feature.assert_called_once()
