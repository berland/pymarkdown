"""
Module to implement a plugin that looks for excessive spaces after the block quote character.
"""
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.plugin_manager import Plugin, PluginDetails


# pylint: disable=too-many-instance-attributes
class RuleMd027(Plugin):
    """
    Class to implement a plugin that looks for excessive spaces after the block quote character.
    """

    def __init__(self):
        super().__init__()
        self.__container_tokens = None
        self.__bq_line_index = None
        self.__last_leaf_token = None
        self.__line_index_at_bq_start = None
        self.__is_paragraph_end_delayed = None
        self.__delayed_blank_line = None
        self.__have_incremented_for_this_line = None
        self.__debug_on = False

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="no-multiple-space-blockquote",
            plugin_id="MD027",
            plugin_enabled_by_default=True,
            plugin_description="Multiple spaces after blockquote symbol",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md027.md",
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__container_tokens = []
        self.__bq_line_index = {}
        self.__last_leaf_token = None
        self.__line_index_at_bq_start = None
        self.__is_paragraph_end_delayed = False
        self.__delayed_blank_line = None
        self.__have_incremented_for_this_line = False

    def __process_delayed_paragraph_end(self, token, num_container_tokens):
        if self.__is_paragraph_end_delayed:
            # if self.__debug_on:
            #     print("[[Processing delayed paragraph end]]")
            #     print(
            #         "delay-para-end-->token->" + ParserHelper.make_value_visible(token)
            #     )
            #     print(
            #         "delay-para-end-->index->"
            #         + str(self.__bq_line_index[num_container_tokens])
            #     )

            # pylint: disable=too-many-boolean-expressions
            assert (
                token.is_blank_line
                or token.is_fenced_code_block
                or token.is_html_block
                or token.is_list_start
                or token.is_atx_heading
                or token.is_block_quote_end
            )
            # pylint: enable=too-many-boolean-expressions
            self.__bq_line_index[num_container_tokens] += 1
            self.__have_incremented_for_this_line = True
            # if self.__debug_on:
            #     print(
            #         "delay-para-end-->index->"
            #         + str(self.__bq_line_index[num_container_tokens])
            #     )
            # if self.__debug_on:
            #     print("[[Delayed paragraph end processed]]")
            self.__is_paragraph_end_delayed = False

    def __process_delayed_blank_line(
        self, context, token, num_container_tokens, allow_block_quote_end
    ):
        if (
            self.__delayed_blank_line
            and not (
                token.is_leaf_end_token
                or (allow_block_quote_end and token.is_block_quote_end)
            )
            and (not self.__have_incremented_for_this_line or token.is_blank_line)
        ):
            self.__have_incremented_for_this_line = False
            self.__handle_blank_line(
                context, self.__delayed_blank_line, num_container_tokens
            )
            self.__delayed_blank_line = None

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """

        if (
            self.__have_incremented_for_this_line
            and not token.is_end_token
            and not token.is_blank_line
        ):
            self.__have_incremented_for_this_line = False

        num_container_tokens = len(
            [i for i in self.__container_tokens if i.is_block_quote_start]
        )
        # if self.__debug_on:
        #     print(
        #         "num->bqs:"
        #         + str(num_container_tokens)
        #         + ", self.__have_incremented_for_this_line="
        #         + str(self.__have_incremented_for_this_line)
        #     )
        #     if num_container_tokens in self.__bq_line_index:
        #         print(
        #             str(self.__bq_line_index[num_container_tokens])
        #             + "-->token>"
        #             + ParserHelper.make_value_visible(token)
        #         )
        #     else:
        #         print("token>" + ParserHelper.make_value_visible(token))
        if token.is_block_quote_start:
            self.__handle_block_quote_start(token)
        elif token.is_block_quote_end:
            self.__handle_block_quote_end(context, token, num_container_tokens)
        elif token.is_list_start:
            self.__handle_list_start(token, num_container_tokens)
        elif token.is_list_end:
            self.__handle_list_end(num_container_tokens)
        elif token.is_new_list_item:
            self.__handle_new_list_item(num_container_tokens)
        elif num_container_tokens:
            self.__handle_within_block_quotes(context, token)

    def __handle_block_quote_start(self, token):
        self.__container_tokens.append(token)

        num_container_tokens = len(
            [i for i in self.__container_tokens if i.is_block_quote_start]
        )
        self.__bq_line_index[num_container_tokens] = 0
        self.__is_paragraph_end_delayed = False
        # if self.__debug_on:
        #     print("bq>" + str(self.__container_tokens[-1]).replace("\n", "\\n"))

    def __handle_block_quote_end(self, context, token, num_container_tokens):
        self.__process_delayed_paragraph_end(token, num_container_tokens)
        self.__process_delayed_blank_line(context, token, num_container_tokens, False)

        num_container_tokens = len(
            [i for i in self.__container_tokens if i.is_block_quote_start]
        )
        # if self.__debug_on:
        #     print(
        #         "leading_spaces>"
        #         + ParserHelper.make_value_visible(
        #             self.__container_tokens[-1].leading_spaces
        #         )
        #     )
        newlines_in_container = self.__container_tokens[-1].leading_spaces.count("\n")
        if (
            not (
                self.__container_tokens[-1].leading_spaces
                and self.__container_tokens[-1].leading_spaces.endswith("\n")
            )
            and self.__container_tokens
            and self.__container_tokens[-1].leading_spaces
        ):
            # if self.__debug_on:
            #     print("newlines_in_container>" + str(newlines_in_container))
            newlines_in_container += 1

        # if self.__debug_on:
        #     print("newlines_in_container>" + str(newlines_in_container))
        #     print("__bq_line_index>" + str(self.__bq_line_index[num_container_tokens]))
        assert newlines_in_container == self.__bq_line_index[num_container_tokens], (
            str(newlines_in_container)
            + " == "
            + str(self.__bq_line_index[num_container_tokens])
        )
        del self.__bq_line_index[num_container_tokens]
        del self.__container_tokens[-1]

    def __handle_list_start(self, token, num_container_tokens):
        self.__process_delayed_paragraph_end(token, num_container_tokens)
        self.__container_tokens.append(token)

    def __handle_new_list_item(self, num_container_tokens):
        # if self.__debug_on:
        #     print(
        #         f"num_container_tokens={num_container_tokens}, __is_paragraph_end_delayed={self.__is_paragraph_end_delayed}, self.__have_incremented_for_this_line={self.__have_incremented_for_this_line}"
        #     )
        if (
            num_container_tokens
            and not self.__have_incremented_for_this_line
            and self.__is_paragraph_end_delayed
        ):
            self.__bq_line_index[num_container_tokens] += 1
            self.__is_paragraph_end_delayed = False

    def __handle_list_end(self, num_container_tokens):
        assert not (
            num_container_tokens
            and not self.__is_paragraph_end_delayed
            and not self.__have_incremented_for_this_line
        )
        # self.__bq_line_index[num_container_tokens] += 1
        del self.__container_tokens[-1]

    def __handle_blank_line(self, context, token, num_container_tokens):
        # if self.__debug_on:
        #     print(f"__handle_blank_line>>{token}<<")
        if token.extracted_whitespace:
            # if self.__debug_on:
            #     print("blank-error")
            self.report_next_token_error(context, token)
        self.__bq_line_index[num_container_tokens] += 1

    def __handle_thematic_break(self, context, token, num_container_tokens):
        if token.extracted_whitespace:
            column_number_delta = -(
                token.column_number - len(token.extracted_whitespace)
            )
            self.report_next_token_error(
                context, token, column_number_delta=column_number_delta
            )
        self.__bq_line_index[num_container_tokens] += 1
        self.__last_leaf_token = token

    def __handle_atx_heading(self, context, token, num_container_tokens):
        if token.extracted_whitespace:
            column_number_delta = -(
                token.column_number - len(token.extracted_whitespace)
            )
            self.report_next_token_error(
                context, token, column_number_delta=column_number_delta
            )
        self.__bq_line_index[num_container_tokens] += 1
        self.__last_leaf_token = token

    def __handle_setext_heading(self, context, token):
        if token.extracted_whitespace:
            line_number_delta = token.original_line_number - token.line_number
            column_number_delta = -(
                token.original_column_number - len(token.extracted_whitespace)
            )
            # if self.__debug_on:
            #     print("setext-error")
            #     print(
            #         "line->"
            #         + str(token.original_line_number)
            #         + ",col="
            #         + str(token.original_column_number)
            #     )
            #     print(
            #         "delta->line->"
            #         + str(line_number_delta)
            #         + ",col="
            #         + str(column_number_delta)
            #     )
            self.report_next_token_error(
                context,
                token,
                line_number_delta=line_number_delta,
                column_number_delta=column_number_delta,
            )
        self.__last_leaf_token = token

    def __handle_setext_heading_end(self, context, token, num_container_tokens):
        if token.extracted_whitespace:
            column_number_delta = -(
                self.__last_leaf_token.column_number - len(token.extracted_whitespace)
            )
            self.report_next_token_error(
                context, self.__last_leaf_token, column_number_delta=column_number_delta
            )
        self.__bq_line_index[num_container_tokens] += 1
        self.__last_leaf_token = None

    def __handle_fenced_code_block(self, context, token, num_container_tokens):
        if token.extracted_whitespace:
            column_number_delta = -(
                token.column_number - len(token.extracted_whitespace)
            )
            # if self.__debug_on:
            #     print("fenced-start-error")
            self.report_next_token_error(
                context, token, column_number_delta=column_number_delta
            )
        self.__last_leaf_token = token
        self.__bq_line_index[num_container_tokens] += 1
        self.__line_index_at_bq_start = self.__bq_line_index[num_container_tokens]

    def __handle_fenced_code_block_end(self, context, token, num_container_tokens):
        if token.extracted_whitespace:
            scoped_block_quote_token = self.__container_tokens[-1]
            split_leading_spaces = scoped_block_quote_token.leading_spaces.split("\n")
            specific_block_quote_prefix = split_leading_spaces[
                self.__bq_line_index[num_container_tokens]
            ]

            line_number_delta = 1 + (
                self.__bq_line_index[num_container_tokens]
                - self.__line_index_at_bq_start
            )
            column_number_delta = -(len(specific_block_quote_prefix) + 1)

            # if self.__debug_on:
            #     print(
            #         "end-container>>"
            #         + ParserHelper.make_value_visible(self.__container_tokens[-1])
            #     )
            #     print(
            #         "split_leading_spaces>>"
            #         + ParserHelper.make_value_visible(split_leading_spaces)
            #     )
            #     print(
            #         "specific_block_quote_prefix>>:"
            #         + ParserHelper.make_value_visible(specific_block_quote_prefix)
            #         + ":"
            #     )
            #     print("fenced-end-error")
            self.report_next_token_error(
                context,
                self.__last_leaf_token,
                line_number_delta=line_number_delta,
                column_number_delta=column_number_delta,
            )
        self.__last_leaf_token = None
        self.__bq_line_index[num_container_tokens] += 1

    def __handle_link_reference_definition(self, context, token, num_container_tokens):
        scoped_block_quote_token = self.__container_tokens[-1]
        if token.extracted_whitespace:
            column_number_delta = -(
                token.column_number - len(token.extracted_whitespace)
            )
            # if self.__debug_on:
            #     print("lrd-1-error")
            self.report_next_token_error(
                context, token, column_number_delta=column_number_delta
            )

        found_index = token.link_destination_whitespace.find("\n")
        if found_index != -1 and ParserHelper.is_character_at_index_whitespace(
            token.link_destination_whitespace, found_index + 1
        ):
            line_number_delta = token.link_name_debug.count("\n") + 1

            split_array_index = (
                self.__bq_line_index[num_container_tokens] + line_number_delta
            )
            split_leading_spaces = scoped_block_quote_token.leading_spaces.split("\n")
            specific_block_quote_prefix = split_leading_spaces[split_array_index]

            column_number_delta = -(len(specific_block_quote_prefix) + 1)

            # if self.__debug_on:
            #     print("line_number_delta>>" + str(line_number_delta))
            #     print("split_array_index>>" + str(split_array_index))
            #     print(
            #         "end-container>>"
            #         + ParserHelper.make_value_visible(self.__container_tokens[-1])
            #     )
            #     print(
            #         "split_leading_spaces>>"
            #         + ParserHelper.make_value_visible(split_leading_spaces)
            #     )
            #     print(
            #         "specific_block_quote_prefix>>:"
            #         + ParserHelper.make_value_visible(specific_block_quote_prefix)
            #         + ":"
            #     )
            #     print("lrd-2-error")
            self.report_next_token_error(
                context,
                token,
                line_number_delta=line_number_delta,
                column_number_delta=column_number_delta,
            )

        found_index = token.link_title_whitespace.find("\n")
        if found_index != -1 and ParserHelper.is_character_at_index_whitespace(
            token.link_title_whitespace, found_index + 1
        ):
            line_number_delta = (
                token.link_name_debug.count("\n")
                + token.link_title_whitespace.count("\n")
                + 1
            )

            split_array_index = (
                self.__bq_line_index[num_container_tokens] + line_number_delta
            )
            split_leading_spaces = scoped_block_quote_token.leading_spaces.split("\n")
            specific_block_quote_prefix = split_leading_spaces[split_array_index]

            column_number_delta = -(len(specific_block_quote_prefix) + 1)
            # if self.__debug_on:
            #     print("line_number_delta>>" + str(line_number_delta))
            #     print("split_array_index>>" + str(split_array_index))
            #     print(
            #         "end-container>>"
            #         + ParserHelper.make_value_visible(self.__container_tokens[-1])
            #     )
            #     print(
            #         "split_leading_spaces>>"
            #         + ParserHelper.make_value_visible(split_leading_spaces)
            #     )
            #     print(
            #         "specific_block_quote_prefix>>:"
            #         + ParserHelper.make_value_visible(specific_block_quote_prefix)
            #         + ":"
            #     )
            #     print("lrd-3-error")
            self.report_next_token_error(
                context,
                token,
                line_number_delta=line_number_delta,
                column_number_delta=column_number_delta,
            )

        self.__bq_line_index[num_container_tokens] += (
            1
            + token.link_name_debug.count("\n")
            + token.link_destination_whitespace.count("\n")
            + token.link_title_whitespace.count("\n")
            + token.link_title_raw.count("\n")
        )

    def __handle_text(self, context, token, num_container_tokens):
        if self.__last_leaf_token.is_setext_heading:
            scoped_block_quote_token = self.__container_tokens[-1]
            for line_number_delta, next_line in enumerate(
                token.end_whitespace.split("\n")
            ):
                found_index = next_line.find(ParserHelper.whitespace_split_character)
                if found_index != -1:
                    next_line = next_line[0:found_index]
                if next_line:
                    split_leading_spaces = (
                        scoped_block_quote_token.leading_spaces.split("\n")
                    )
                    split_array_index = (
                        self.__bq_line_index[num_container_tokens]
                        + line_number_delta
                        + 1
                    )
                    specific_block_quote_prefix = split_leading_spaces[
                        split_array_index
                    ]
                    calculated_column_number = -(len(specific_block_quote_prefix) + 1)

                    # if self.__debug_on:
                    #     print(
                    #         "split_leading_spaces>>"
                    #         + ParserHelper.make_value_visible(split_leading_spaces)
                    #     )
                    #     print(
                    #         "split_array_index>>"
                    #         + ParserHelper.make_value_visible(split_array_index)
                    #     )
                    #     print(
                    #         "specific_block_quote_prefix>>:"
                    #         + ParserHelper.make_value_visible(
                    #             specific_block_quote_prefix
                    #         )
                    #         + ":"
                    #     )
                    #     print("setext-text-error")
                    self.report_next_token_error(
                        context,
                        token,
                        line_number_delta=line_number_delta,
                        column_number_delta=calculated_column_number,
                    )
            self.__bq_line_index[num_container_tokens] += (
                token.end_whitespace.count("\n") + 1
            )
        elif (
            self.__last_leaf_token.is_html_block or self.__last_leaf_token.is_code_block
        ):
            self.__bq_line_index[num_container_tokens] += (
                token.token_text.count("\n") + 1
            )

    def __handle_paragraph(self, context, token, num_container_tokens):
        self.__last_leaf_token = token
        scoped_block_quote_token = self.__container_tokens[-1]

        for line_number_delta, next_line in enumerate(
            token.extracted_whitespace.split("\n")
        ):
            if next_line and scoped_block_quote_token.leading_spaces:
                # if self.__debug_on:
                #     print("1>" + str(self.__bq_line_index[num_container_tokens]))
                #     print("2>" + str(line_number_delta))
                #     print("3>" + str(scoped_block_quote_token).replace("\n", "\\n"))
                split_leading_spaces = scoped_block_quote_token.leading_spaces.split(
                    "\n"
                )
                line_index = (
                    self.__bq_line_index[num_container_tokens] + line_number_delta
                )
                calculated_column_number = len(split_leading_spaces[line_index]) + 1
                # if self.__debug_on:
                #     print("4>" + str(split_leading_spaces).replace("\n", "\\n"))
                #     print("5>" + str(line_index))
                #     print("column>" + str(calculated_column_number))
                #     print("para-error")
                self.report_next_token_error(
                    context,
                    scoped_block_quote_token,
                    line_number_delta=line_number_delta,
                    column_number_delta=-calculated_column_number,
                )
        self.__bq_line_index[num_container_tokens] += token.extracted_whitespace.count(
            "\n"
        )

    # pylint: disable=too-many-branches
    def __handle_within_block_quotes(self, context, token):
        num_container_tokens = len(
            [i for i in self.__container_tokens if i.is_block_quote_start]
        )
        # if self.__debug_on:
        #     print(
        #         ParserHelper.make_value_visible(self.__bq_line_index)
        #         + "-->index>"
        #         + str(num_container_tokens)
        #     )
        #     print(
        #         str(self.__bq_line_index[num_container_tokens])
        #         + "-->token>"
        #         + ParserHelper.make_value_visible(token)
        #     )

        self.__process_delayed_paragraph_end(token, num_container_tokens)
        self.__process_delayed_blank_line(context, token, num_container_tokens, True)

        if token.is_paragraph:
            self.__handle_paragraph(context, token, num_container_tokens)
        elif token.is_text:
            self.__handle_text(context, token, num_container_tokens)
        elif token.is_paragraph_end:
            self.__last_leaf_token = None
            self.__is_paragraph_end_delayed = True
            # if self.__debug_on:
            #     print("[[Delaying paragraph end]]")
        elif token.is_blank_line:
            self.__delayed_blank_line = token
            # if self.__debug_on:
            #     print("[[Delaying blank line]]")
        elif token.is_atx_heading:
            self.__handle_atx_heading(context, token, num_container_tokens)
        elif token.is_setext_heading:
            self.__handle_setext_heading(context, token)
        elif token.is_setext_heading_end:
            self.__handle_setext_heading_end(context, token, num_container_tokens)
        elif token.is_html_block or token.is_indented_code_block:
            self.__last_leaf_token = token
        elif (
            token.is_html_block_end
            or token.is_indented_code_block_end
            or token.is_atx_heading_end
        ):
            self.__last_leaf_token = None
        elif token.is_fenced_code_block:
            self.__handle_fenced_code_block(context, token, num_container_tokens)
        elif token.is_fenced_code_block_end:
            self.__handle_fenced_code_block_end(context, token, num_container_tokens)
        elif token.is_thematic_break:
            self.__handle_thematic_break(context, token, num_container_tokens)
        elif token.is_link_reference_definition:
            self.__handle_link_reference_definition(
                context, token, num_container_tokens
            )
        # if self.__debug_on:
        #     print(
        #         str(self.__bq_line_index[num_container_tokens])
        #         + "<--token>"
        #         + ParserHelper.make_value_visible(token)
        #     )

    # pylint: enable=too-many-branches


# pylint: enable=too-many-instance-attributes
