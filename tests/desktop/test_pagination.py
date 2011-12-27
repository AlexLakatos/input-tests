#!/usr/bin/env python

# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Mozilla WebQA Tests.
#
# The Initial Developer of the Original Code is Mozilla.
#
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Dave Hunt <dhunt@mozilla.com>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

from unittestzero import Assert
import pytest

from pages.desktop.feedback import FeedbackPage
from pages.desktop.themes import ThemesPage

xfail = pytest.mark.xfail
nondestructive = pytest.mark.nondestructive


class TestPagination:

    @xfail(reason="Bug 617177 - Filter type (happy/sad) doesn't persist when paginating through Themes")
    @nondestructive
    def test_themes_filters_persist_when_paging_through_results(self, mozwebqa):
        """This testcase covers # 15018 in Litmus.

        1. Verifies the filter is in the URL
        2. Verifies the currently applied filter is styled appropriately
        3. Verifies the results of the filter

        """
        themes_pg = ThemesPage(mozwebqa)

        themes_pg.go_to_themes_page()
        themes_pg.type_filter.click_issues()
        themes_pg.click_older_messages()
        Assert.equal(themes_pg.feedback_type_from_url, "issue")
        Assert.equal(themes_pg.type_filter.selected_type, "Issues")
        [Assert.equal(theme.type, "Issue") for theme in themes_pg.themes]

    @nondestructive
    def test_search_pagination(self, mozwebqa):
        """Litmus 13636 - Input: Verify Search results have pagination."""
        feedback_pg = FeedbackPage(mozwebqa)
        feedback_pg.go_to_feedback_page()
        feedback_pg.search_for("facebook")

        Assert.true(feedback_pg.is_older_messages_link_visible)
        Assert.true(feedback_pg.is_newer_messages_link_visible)
        Assert.false(feedback_pg.is_newer_messages_link_enabled)

        Assert.equal(feedback_pg.older_messages_link, u"\xab Older Messages")
        Assert.equal(feedback_pg.newer_messages_link, u"Newer Messages \xbb")

        for var in range(2, 12):
            feedback_pg.click_older_messages()
            Assert.equal(feedback_pg.product_from_url, "firefox")
            Assert.equal(feedback_pg.search_term_from_url, "facebook")

            Assert.true(feedback_pg.is_older_messages_link_visible)
            Assert.true(feedback_pg.is_newer_messages_link_visible)

            Assert.true(feedback_pg.is_older_messages_link_enabled)
            Assert.true(feedback_pg.is_newer_messages_link_enabled)

            Assert.equal(feedback_pg.older_messages_link, u"\xab Older Messages")
            Assert.equal(feedback_pg.newer_messages_link, u"Newer Messages \xbb")

            Assert.equal(int(feedback_pg.page_from_url), var)