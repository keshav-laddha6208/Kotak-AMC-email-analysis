import streamlit as st
import pandas as pd
import plotly.express as px

import os
os.chdir("C:\\Users\\kesha\\Downloads\\")

#Title for the Page
st.set_page_config(
    page_title = "Kotak AMC Analysis",
    layout = "wide"
)

#Reading the excel sheet and creating a dataframe
filepath = "master_data.xlsx"
df = pd.read_excel(filepath, sheet_name = "Master Data")

#Main title of the report
st.title("Email Analysis: Kotak AMC vis-à-vis Competitors for FY 2025–26")

#creating a sidebar titled Filters to filter the selected AMC or Category
st.sidebar.header("Filters")
selected_amcs = st.sidebar.multiselect(
    "Select AMC",
    df["Company name"].unique(),
    default = df["Company name"].unique()
)

selected_categories = st.sidebar.multiselect(
    "Select Category",
    df["Categorisation"].unique(),
    default = df["Categorisation"].unique()
)

#creating a variable to save the filtered AMCs and Categories
filtered_df = df[
    (df["Company name"].isin(selected_amcs)) &
    (df["Categorisation"].isin(selected_categories))
    ]


#creating cards in the form of 3 columns for avg read rate, inbox placement and delete rate
col1, col2, col3 = st.columns(3)
col1.metric(
    "Average Read Rate",
    round(filtered_df["read_rate"].mean(), 2)
)
col2.metric(
    "Average Inbox Placement",
    round(filtered_df["overall_inbox_placement"].mean(), 2)
)
col3.metric(
    "Average Delete Rate",
    round(filtered_df["delete_rate"].mean(), 2)
)


#creating a stacked bar chart using group by and px.bar func of email count by category per AMC
email_count = df.groupby(
    ['Company name', 'Categorisation']
).size().reset_index(name = 'Count')

fig3 = px.bar(
    email_count,
    x = 'Company name',
    y = 'Count',
    color = 'Categorisation',
    barmode = 'stack',
    title = 'Email count by Category Across AMCs (FY 25-26)',
    labels = {'Company name': 'AMC', 'Count': 'Number of Emails'}
)

fig3.update_layout(
    legend_title = 'Category',
    width = 1000,
    height = 600
)

st.plotly_chart(fig3, config={"responsive": True})
st.info("💡 **Key Takeaway:** Nippon India dominates email volume at ~2,250 emails — nearly 3x the next highest AMC. Edelweiss has the lowest send volume in the peer set.")

with st.expander("📝 Detailed Commentary"):
    st.markdown("""
    - **Nippon India** is a clear outlier in volume, with Fund and SIP emails forming the bulk of its sends.
    - **ABSL, ICICI Pru, and Kotak** form the mid-volume tier (~750–900 emails), each with a reasonably diversified category mix.
    - **ICICI Pru** stands out in this tier for its high SIP and Service email proportion relative to peers.
    - **Kotak** has a relatively higher Fund email proportion compared to most peers, with limited Service and Webinar presence in its mix.
    - **DSP, Edelweiss, and Axis** are low-volume senders (~130–430 emails), likely running more targeted or selective campaigns.
    - **Service emails** (green) are visible primarily at ICICI Pru and SBI — most other AMCs show minimal service email activity.
    - **Webinar emails** are a negligible share of volume across all AMCs, despite their outsized read rate performance.
    - High volume does not correlate with high read rates — Nippon India's dominance here should be cross-referenced against the read rate charts.
    """)

with st.expander("📌 Kotak Spotlight"):
    st.markdown("""
    - Kotak sits in the mid-volume tier alongside ABSL and ICICI Pru, sending approximately 750 emails — well below Nippon India but ahead of smaller senders like DSP, Edelweiss, and Axis.
    - Kotak's volume is dominated by Fund emails, with relatively limited investment in Service and Webinar categories — two areas where peers like ICICI Pru and SBI show stronger presence.
    - The near-absence of Webinar emails in Kotak's mix is a notable gap, given that Webinar emails deliver disproportionately high read rates across the peer set.
    """)

#creating a stacked bar chart of % distribution of email categories vs. total emails sent
email_counts = pd.crosstab(
    df['Company name'],
    df['Categorisation']
)
email_pct = (email_counts.div(email_counts.sum(axis = 1), axis=0) * 100).reset_index()

long_df = email_pct.melt(
    id_vars='Company name',
    var_name='Category',
    value_name='Percentage'
)

fig4 = px.bar(
    long_df,
    x = 'Company name',
    y = 'Percentage',
    color = 'Category',
    title = 'Email Category Mix by AMC (%)'
)

fig4.update_layout(
    barmode = 'stack',
    yaxis_title = 'Percentage of Total Emails',
    xaxis_title = 'AMC'
)

st.plotly_chart(fig4, config={"responsive": True})
st.info("💡 **Key Takeaway:** No two AMCs share the same category mix, reflecting distinctly different communication strategies across the peer set.")

with st.expander("📝 Detailed Commentary"):
    st.markdown("""
    - **DSP** has the most unusual mix in the peer set — Webinar emails account for the single largest share of its sends, with relatively low Fund and SIP presence.
    - **ICICI Pru** is the most Outlook-heavy AMC, with Outlook emails forming nearly half its total volume, suggesting a strong focus on market commentary and investor education content.
    - **Nippon India** has the highest SIP email proportion across all AMCs, indicating a clear strategic emphasis on SIP acquisition and retention messaging.
    - **SBI** allocates the largest share to Service emails among all peers, reflecting a more transactional, customer-servicing communication approach.
    - **ABSL, Axis, HDFC, and Kotak** follow a broadly similar pattern — Fund emails form the largest single category, with SIP and Outlook as secondary categories.
    - **Edelweiss** stands out for an almost complete absence of Fund and SIP emails, with its mix dominated by Webinar and Service content — the most distributor-focused strategy in the peer set.
    - **Generic emails** are a negligible share across all AMCs, suggesting the peer set has largely moved away from unstructured broadcast communication.
    """)

with st.expander("📌 Kotak Spotlight"):
    st.markdown("""
    - Kotak's category mix is Fund-heavy, similar to ABSL and Axis, but unlike ICICI Pru 
      and SBI which allocate significantly more to Outlook and Service emails respectively.
    - Kotak has minimal Webinar and Service presence — two categories that drive strong 
      read rates for peers like DSP and ICICI Pru.
    """)


#creating avg inbox placement per AMC bar chart using the filtered dataframe
inbox_chart = filtered_df.groupby(
    "Company name"
)["overall_inbox_placement"].mean().reset_index()

fig4 = px.bar(
    inbox_chart,
    x = 'Company name',
    y = 'overall_inbox_placement',
    title = 'Inbox Placement by AMC'
)

st.plotly_chart(fig4, config={"responsive": True})

st.info("💡 **Key Takeaway:** HDFC leads inbox placement at ~86%, while ABSL is the weakest at ~52% — a 34 percentage point gap across the peer set.")

with st.expander("📝 Detailed Commentary"):
    st.markdown("""
    - **HDFC** leads the peer set with the highest inbox placement at ~86%, the only AMC to cross the 85% mark.
    - **Axis, ICICI Pru, and SBI** form a strong second tier, all delivering inbox placement in the 80–82% range.
    - **DSP, Edelweiss, and Nippon India** cluster in the 60–62% range — a significant drop from the top tier, indicating deliverability challenges relative to peers.
    - **ABSL** is the weakest performer at ~52%, the only AMC to fall below 60% inbox placement in the peer set.
    - There is no direct correlation between email volume and inbox placement — HDFC achieves the highest placement despite mid-range volume, while high-volume sender Nippon India sits in the lower tier.
    """)

with st.expander("📌 Kotak Spotlight"):
    st.markdown("""
    - Kotak's inbox placement of ~67% places it fifth in the peer set, below the top tier of HDFC, Axis, ICICI Pru, and SBI.
    - Kotak trails the peer set leader HDFC by ~19 percentage points.
    - Kotak outperforms DSP, Edelweiss, Nippon India, and ABSL on inbox placement, but remains well below the 80%+ club.
    - Kotak is the only mid-volume AMC that does not achieve 80%+ inbox placement — Axis and ICICI Pru at similar volumes both cross that threshold.
    """)


#creating a bar chart using the filtered dataframe showing avg read rate per AMC
amc_read = filtered_df.groupby(
    "Company name"
)["read_rate"].mean().reset_index()

fig = px.bar(
    amc_read,
    x = "Company name",
    y = "read_rate",
    title = "Average Read Rate by AMC"
)
st.plotly_chart(fig, config={"responsive": True})

st.info("💡 **Key Takeaway:** ICICI Pru leads the peer set with an average read rate of ~26%, nearly 1.4x higher than the second-ranked SBI at ~19%. ABSL and Nippon India are the weakest performers at ~7%.")

with st.expander("📝 Detailed Commentary"):
    st.markdown("""
    - **ICICI Pru** is a clear outlier, with an average read rate significantly above all peers — driven by its distributor-targeted webinar emails and strong audience segmentation.
    - **SBI** is the second strongest performer, likely lifted by its high Service email proportion which consistently delivers above-average read rates.
    - **Edelweiss, DSP, and Axis** form a mid-tier cluster in the 11–13% range, punching above their weight relative to their low send volumes.
    - **HDFC, Kotak, and Nippon India** sit in the 7–10% band, underperforming relative to the peer average despite varying volume levels.
    - **ABSL** is the weakest performer in the set at ~7%, suggesting either a broad untargeted audience, a category mix skewed toward lower-performing email types, or both.
    - High send volume does not correlate with high read rates — Nippon India sends the most emails in the peer set but ranks among the lowest for read rate.
    """)

with st.expander("📌 Kotak Spotlight"):
    st.markdown("""
    - Kotak's average read rate of ~10% places it in the bottom half of the peer set, ahead of only ABSL, HDFC, and Nippon India.
    - Kotak trails the peer set leader ICICI Pru by ~16 percentage points — a significant gap that warrants a deeper look at audience segmentation and category mix.
    - Kotak's Fund-heavy email mix, combined with limited Webinar and Service presence, is a likely contributor to its below-average read rate performance.
    - Improving read rates will require either a shift in category mix toward higher-performing types (Service, Webinar) or stronger subject line and personalisation strategies within existing categories.
    """)


#creating category wise read rate comparision using the filtered dataframe
category_chart = filtered_df.groupby(
    ["Company name", "Categorisation"]
)["read_rate"].mean().reset_index()

fig2 = px.bar(
    category_chart,
    x = "Categorisation",
    y = "read_rate",
    color = "Company name",
    barmode = "group",
    title = "Category-wise Read Rate Comparision"
)
st.plotly_chart(fig2, config={"responsive": True})

st.info("💡 **Key Takeaway:** Service and Webinar are the highest-performing categories across the peer set. Fund and SIP consistently deliver the lowest read rates across all AMCs.")

with st.expander("📝 Detailed Commentary"):
    st.markdown("""
    - **Service emails** deliver the highest read rates across the peer set — ICICI Pru leads at ~34%, followed closely by SBI at ~30%. Every AMC that sends Service emails outperforms its own average in this category.
    - **Webinar emails** are the second strongest category — SBI leads at ~29%, with Edelweiss and Kotak also showing strong performance relative to their overall averages.
    - **Outlook emails** show the widest performance gap across AMCs — ICICI Pru leads at ~26% while most peers cluster between 6–16%, indicating execution quality varies significantly in this category.
    - **Generic emails** show a similar wide spread — Axis leads at ~20% while Nippon India and Kotak trail at ~5–7%.
    - **Fund and SIP emails** are the lowest-performing categories across all AMCs, with most players delivering read rates in the 7–12% range.
    - **ICICI Pru** is the top performer in Fund, Outlook, and Service categories simultaneously — the only AMC to lead in three categories.
    """)

with st.expander("📌 Kotak Spotlight"):
    st.markdown("""
    - Kotak's best performing category is Webinar (~11%), followed by Service (~13%) — both above its overall average of ~10%.
    - Kotak ranks among the lower performers in Fund (~8%), Generic (~7%), and Outlook (~9%) categories.
    - Kotak trails the category leader in every single category — the gap is largest in Service (ICICI Pru at ~34% vs Kotak at ~13%) and Outlook (ICICI Pru at ~26% vs Kotak at ~9%).
    - SIP is Kotak's weakest category at ~8%, in line with the peer set trend of low SIP read rates overall.
    """)



#creating a read rate heatmap by first making a pivot table and then converting it into a heatmap
pivot = pd.pivot_table(
    filtered_df,
    values = 'read_rate',
    index = 'Company name',
    columns = 'Categorisation',
    aggfunc = 'mean'
).round(2)

fig5 = px.imshow(
    pivot,
    text_auto = True,
    aspect = 'auto',
    title = 'Read Rate Heatmap'
)

st.plotly_chart(fig5, config={"responsive": True})

st.info("💡 **Key Takeaway:** ICICI Pru records the highest read rate in 4 out of 6 categories — Fund (18.13%), Outlook (26.67%), Service (34.16%), and Webinar (29.13%). ABSL records a 0% Service read rate, the only zero in the entire heatmap.")

with st.expander("📝 Detailed Commentary"):
    st.markdown("""
    - **ICICI Pru** dominates across categories — its Service (34.16%) and Webinar (29.13%) read rates are the highest in the peer set by a significant margin.
    - **SBI** is the second strongest overall performer — it leads in SIP (16.76%) and Service (29.73%), and delivers above-average read rates across all six categories.
    - **Axis** records the highest Generic read rate at 19.49%, outperforming all peers in that category by a wide margin.
    - **DSP** leads the Outlook category among non-ICICI peers at 15.86%, and delivers consistently above-average performance across Fund, Outlook, and SIP.
    - **Edelweiss** leads the peer set in Webinar after ICICI Pru at 13.26%, and also records strong Service performance at 21.42%.
    - **Nippon India** is the weakest performer across the most categories — recording the lowest or near-lowest read rates in Fund, Generic, Outlook, Service, and Webinar.
    - **ABSL** records a 0% Service read rate — the only zero value in the entire heatmap, indicating no Service emails were read or no Service emails were sent in the analysis period.
    - **HDFC** delivers consistent but mid-range performance across all categories, with no standout highs or lows.
    """)

with st.expander("📌 Kotak Spotlight"):
    st.markdown("""
    - Kotak's strongest category is Service at 13.32%, followed by Webinar at 11.24% and SIP at 10.74%.
    - Kotak's weakest category is Generic at 7.28%, the third lowest in the peer set for that category.
    - Kotak does not lead in any single category across the peer set.
    - Kotak trails ICICI Pru in every category — the largest gaps are in Service (34.16% vs 13.32%) and Webinar (29.13% vs 11.24%).
    - Kotak's Fund read rate of 9.97% is mid-table, ahead of ABSL, HDFC, and Nippon India but behind ICICI Pru, SBI, Edelweiss, DSP, and Axis.
    """)


#creating a inbox placement heatmap by first making a pivot table and then converting it into a heatmap
pivot2 = pd.pivot_table(
    filtered_df,
    values = "overall_inbox_placement",
    index = 'Company name',
    columns = 'Categorisation',
    aggfunc = 'mean'
).round(2)

fig6 = px.imshow(
    pivot2,
    text_auto = True,
    aspect = 'auto',
    title = 'Inbox Placement Heatmap'
)
st.plotly_chart(fig6, config={"responsive": True})

st.info("💡 **Key Takeaway:** HDFC leads inbox placement across nearly every category, peaking at 99.73% in Service. ABSL is the weakest performer across all six categories, dropping as low as 40% in Service.")

with st.expander("📝 Detailed Commentary"):
    st.markdown("""
    - **HDFC** records the highest inbox placement in 5 out of 6 categories — Fund (91.42%), Outlook (86.45%), SIP (90.99%), Service (99.73%), and Webinar (82.43%), making it the strongest deliverability performer in the peer set.
    - **Axis and SBI** form a strong second tier, consistently delivering inbox placement in the 80–86% range across all categories.
    - **ICICI Pru** delivers solid inbox placement across all categories (74–88%), with Service at 88.38% being its strongest.
    - **DSP, Edelweiss, and Nippon India** cluster in the 55–67% range across most categories, with Edelweiss recording the lowest SIP inbox placement at 45.33%.
    - **ABSL** is the weakest performer across all six categories — its highest placement is 54.11% in Fund, and it drops to 40% in Service, the lowest single value in the entire heatmap.
    - Inbox placement is consistently high across all categories for top-tier AMCs, indicating that deliverability performance is an AMC-level characteristic rather than a category-specific one.
    """)

with st.expander("📌 Kotak Spotlight"):
    st.markdown("""
    - Kotak's inbox placement ranges from 64.87% (Fund) to 72.59% (Service) across all six categories — a narrow band indicating consistent but mid-range deliverability.
    - Kotak does not lead in any category and trails the peer set leader HDFC by 20–27 percentage points across all categories.
    - Kotak outperforms ABSL, DSP, Edelweiss, and Nippon India across all categories but sits below HDFC, Axis, SBI, and ICICI Pru in every category.
    - Kotak's Service inbox placement of 72.59% is its strongest category but still 27 percentage points below HDFC's 99.73% in the same category.
    """)


#creating a delete rate heatmap by first making a pivot table and then converting it into a heatmap
pivot3 = pd.pivot_table(
    filtered_df,
    values = 'delete_rate',
    index = 'Company name',
    columns = 'Categorisation',
    aggfunc = 'mean'
).round(2)

fig7 = px.imshow(
    pivot3,
    text_auto = True,
    aspect = 'auto',
    title = 'Delete Rate Heatmap'
)
st.plotly_chart(fig7, config={"responsive": True})

st.info("💡 **Key Takeaway:** ICICI Pru records the highest delete rate in Outlook at 34.1% and ABSL peaks at 33.33% in Service — the two highest single values in the heatmap. HDFC and DSP record the lowest Service delete rates at 4.61% and 9.91% respectively.")

with st.expander("📝 Detailed Commentary"):
    st.markdown("""
    - **ICICI Pru** records the highest Outlook delete rate at 34.1% — notably high given that it also leads Outlook read rates, indicating a polarised audience response to its Outlook emails.
    - **ABSL** records the highest Service delete rate at 33.33% — the second highest single value in the heatmap and a stark contrast to its 0% Service read rate.
    - **HDFC** records the lowest Service delete rate at 4.61%, the lowest single value in the entire heatmap, consistent with its strong inbox placement performance.
    - **SBI** records the lowest Service delete rate among high-volume AMCs at 5.92%, alongside its strong Service read rate of 29.73%.
    - **Edelweiss** delivers the lowest delete rates in Generic (8.57%) and SIP (8.12%) categories, the strongest performance in those two categories across the peer set.
    - **DSP** records the lowest Service delete rate after HDFC at 9.91%, and delivers consistently below-average delete rates across most categories.
    - **Axis** records the highest Fund delete rate at 17.48% and the highest SIP delete rate at 18.88% among all peers.
    - Delete rates are elevated in Outlook and Webinar categories across most AMCs, indicating these are the categories with the most polarised recipient responses.
    """)

with st.expander("📌 Kotak Spotlight"):
    st.markdown("""
    - Kotak's delete rates range from 11.82% (Webinar) to 15.51% (Fund) — a mid-range band with no extreme highs or lows relative to peers.
    - Kotak's lowest delete rate is in Webinar (11.82%), consistent with Webinar being one of its stronger read rate categories.
    - Kotak's highest delete rate is in Fund (15.51%), its most heavily sent category — indicating a segment of recipients consistently discarding Fund emails.
    - Kotak does not record the highest or lowest delete rate in any single category across the peer set.
    - Kotak's Service delete rate of 14.35% is mid-table — higher than HDFC (4.61%), SBI (5.92%), DSP (9.91%), and ICICI Pru (10.06%), but lower than ABSL (33.33%), Edelweiss (19.34%), and Nippon India (15.96%).
    """)


#creating a read delete heatmap by first making a pivot table and then converting it into a heatmap
pivot4 = pd.pivot_table(
    filtered_df,
    values = 'read_delete_rate',
    index = 'Company name',
    columns = 'Categorisation',
    aggfunc = 'mean'
).round(2)

fig8 = px.imshow(
    pivot4,
    text_auto = True,
    aspect = 'auto',
    title = 'Read Delete Rate Heatmap'
)
st.plotly_chart(fig8, config={"responsive": True})

st.info("💡 **Key Takeaway:** ICICI Pru records the highest read-delete rates in Generic (8%), Outlook (10.9%), and Webinar (8.57%) — the three highest single values in the heatmap. ABSL records a 0% Service read-delete rate, and Nippon India records the lowest values across the most categories.")

with st.expander("📝 Detailed Commentary"):
    st.markdown("""
    - **ICICI Pru** dominates the read-delete metric — its Outlook read-delete rate of 10.9% is the highest single value in the entire heatmap, indicating a significant portion of its Outlook audience reads but then deletes the email.
    - **DSP** records the highest Service read-delete rate at 9.52%, the second highest single value in the heatmap.
    - **Nippon India** records the lowest or near-lowest read-delete rates across Fund (3.19%), Generic (2.36%), Outlook (1.26%), Service (1.24%), and Webinar (1.73%) — the weakest performer across the most categories.
    - **ABSL** records a 0% Service read-delete rate, consistent with its 0% Service read rate — confirming no Service email engagement of any kind for ABSL in the analysis period.
    - **Axis** leads the Generic read-delete category at 4.58% and Service at 6.49%, indicating above-average post-read discard behaviour in those categories.
    - Read-delete rates are uniformly low across all AMCs and categories (mostly 2–5%), with ICICI Pru's Outlook at 10.9% being the only value to cross the 10% mark.
    - The overall low read-delete rates across the peer set indicate that recipients who open emails generally do not delete them immediately after reading.
    """)

with st.expander("📌 Kotak Spotlight"):
    st.markdown("""
    - Kotak's read-delete rates range from 2.98% (Generic) to 4.84% (Fund) — consistently mid-range with no outlier values in any category.
    - Kotak's highest read-delete rate is in Fund (4.84%), its most heavily sent category.
    - Kotak's Service read-delete rate of 3.53% is mid-table — lower than DSP (9.52%), Axis (6.49%), and ICICI Pru (9%) but higher than Nippon India (1.24%), ABSL (0%), Edelweiss (4%), and HDFC (4.42%).
    - Kotak does not record the highest or lowest read-delete rate in any single category across the peer set.
    """)


#creating a email count heatmap by first making a pivot table and then converting it into a heatmap
pivot5 = pd.pivot_table(
    email_count,
    values = 'Count',
    index = 'Company name',
    columns = 'Categorisation',
    aggfunc = 'mean'
).round(2)

fig9 = px.imshow(
    pivot5,
    text_auto = True,
    aspect = 'auto',
    title = 'Email count Heatmap'
)
st.plotly_chart(fig9, config={"responsive": True})

st.info("💡 **Key Takeaway:** Nippon India dominates volume in Fund (1143) and SIP (544) — the two highest single values in the heatmap by a significant margin. ICICI Pru leads Outlook volume at 345 and Service volume at 214.")

with st.expander("📝 Detailed Commentary"):
    st.markdown("""
    - **Nippon India** is the volume leader in Fund (1143) and SIP (544) by a wide margin — its Fund count alone exceeds the total email count of several peers in the set.
    - **ICICI Pru** leads in Outlook (345) and Service (214), reflecting its strategic focus on market commentary and transactional communication.
    - **SBI** is the second highest SIP sender at 341, and also records strong Service volume at 137 — the second highest in the peer set after ICICI Pru.
    - **ABSL** leads Generic volume at 225 and is the second highest Fund sender at 403, with a near-zero Service presence (1 email).
    - **DSP** is the highest Webinar sender at 101 emails, consistent with its category mix being Webinar-heavy relative to peers.
    - **Edelweiss** sends the fewest emails overall — recording single-digit or low double-digit counts across most categories.
    - **HDFC** maintains a relatively balanced distribution across Fund (96), Generic (123), and Outlook (97) with minimal SIP and Service volume.
    - **Axis** concentrates volume in Fund (238) and Service (85), with very low counts in Generic (15), Outlook (22), SIP (29), and Webinar (24).
    """)

with st.expander("📌 Kotak Spotlight"):
    st.markdown("""
    - Kotak's highest volume category is Fund at 327 emails, the third highest Fund count in the peer set after Nippon India (1143) and ABSL (403).
    - Kotak's second highest category is Outlook at 166, followed by SIP at 157 — indicating a three-category concentration strategy.
    - Kotak's Service volume of 66 and Webinar volume of 16 are among the lower counts in the peer set for those categories.
    - Kotak sends the fewest Webinar emails among mid-to-high volume AMCs, with only Edelweiss (47) and Axis (24) sending fewer in absolute terms among peers with comparable overall volume.
    - Kotak's Generic count of 35 is low, consistent with its below-average Generic read rate performance.
    """)


#creating a email count percentage heatmap by first making a pivot table and then converting it into a heatmap
pivot6 = pd.pivot_table(
    email_count,
    values = 'Count',
    index = 'Company name',
    columns = 'Categorisation',
    aggfunc = 'sum'
).round(2)

pivot6_pct = pivot6.div(pivot6.sum(axis=1), axis=0).mul(100).round(2)

fig10 = px.imshow(
    pivot6_pct,
    text_auto = True,
    aspect = 'auto',
    title = 'Email count (%) Heatmap'
)
st.plotly_chart(fig10, config={"responsive": True})

st.info("💡 **Key Takeaway:** Every AMC has a single dominant category that accounts for the largest share of its sends — and no two AMCs share the same dominant category, reflecting nine distinct communication strategies across the peer set.")

with st.expander("📝 Detailed Commentary"):
    st.markdown("""
    - **DSP** allocates 56.42% of its sends to Webinar — the highest single-category concentration in the entire heatmap, making it the most Webinar-dependent AMC by a significant margin.
    - **SBI** allocates 53.36% of its sends to SIP — the second highest single-category concentration, indicating a clear strategic focus on SIP-driven communication.
    - **ICICI Pru** allocates 43.07% of its sends to Outlook — the highest Outlook concentration in the peer set, consistent with its market commentary-heavy communication approach.
    - **Axis** allocates 57.63% of its sends to Fund — the highest Fund concentration in the peer set, with Service (20.58%) as its only meaningful secondary category.
    - **Nippon India** allocates 51.05% to Fund and 24.3% to SIP — a two-category concentration accounting for over 75% of total sends.
    - **ABSL** allocates 45.69% to Fund and 25.51% to Generic — the highest Generic concentration in the peer set, with near-zero Service presence (0.11%).
    - **HDFC** has the most balanced distribution in the peer set — Fund (23.13%), Generic (29.64%), and Outlook (23.37%) together account for ~76% of sends with no single category exceeding 30%.
    - **Edelweiss** is the only AMC where Webinar (33.81%) and Outlook (25.18%) together form the majority of sends, with Fund at just 24.46%.
    """)

with st.expander("📌 Kotak Spotlight"):
    st.markdown("""
    - Kotak's sends are concentrated in three categories — Fund (42.63%), Outlook (21.64%), and SIP (20.47%) — which together account for ~85% of total sends.
    - Kotak has the second highest Fund concentration in the peer set after Axis (57.63%).
    - Kotak's Service allocation of 8.6% and Webinar allocation of 2.09% are among the lowest in the peer set — two categories that deliver above-average read rates for peers investing in them.
    - Kotak's category mix is the most Fund-and-Outlook concentrated among mid-volume AMCs — unlike ICICI Pru which balances Outlook with strong Service presence, or SBI which balances SIP with strong Service presence.
    """)


#creating a table ranking AMCs acc to the read rate
ranking = filtered_df.groupby("Company name")["read_rate"].mean().reset_index()
ranking = round(ranking.sort_values("read_rate", ascending = False).reset_index(drop = True), 2)
st.subheader("AMC Ranking according to Read Rate")
ranking.index = range(1, len(ranking) + 1)
st.dataframe(ranking)


#creating a table ranking AMCs acc to the delete rate
ranking_dr = filtered_df.groupby("Company name")["delete_rate"].mean().reset_index()
ranking_dr = round(ranking_dr.sort_values("delete_rate", ascending = False).reset_index(drop = True), 2)
st.subheader("AMC Ranking according to Delete Rate")
ranking_dr.index = range(1, len(ranking_dr) + 1)
st.dataframe(ranking_dr)


#creating a table ranking AMCs acc to the inbox placement
ranking_ip = filtered_df.groupby("Company name")["overall_inbox_placement"].mean().reset_index()
ranking_ip = round(ranking_ip.sort_values("overall_inbox_placement", ascending = False).reset_index(drop = True),2)
st.subheader("AMC Ranking according to Inbox Placement")
ranking_ip.index = range(1, len(ranking_ip) + 1)
st.dataframe(ranking_ip)


#creating a table ranking AMCs acc to the read delete rate
ranking_rdr = filtered_df.groupby("Company name")["read_delete_rate"].mean().reset_index()
ranking_rdr = round(ranking_rdr.sort_values("read_delete_rate", ascending = False).reset_index(drop = True), 2)
st.subheader("AMC Ranking according to Read Delete Rate")
ranking_rdr.index = range(1, len(ranking_rdr) + 1)
st.dataframe(ranking_rdr)


#category specific AMC ranking
st.subheader("Category Specific AMC rankings")
selected_category = st.selectbox('Select Category', options=df['Categorisation'].unique().tolist())
filtered_df = df[df['Categorisation'] == selected_category]

#Read Rate Ranking 
read_rate_df = (
    filtered_df.groupby('Company name')['read_rate']
    .mean()
    .reset_index()
    .rename(columns={'read_rate': 'Avg Read Rate (%)'})
    .sort_values('Avg Read Rate (%)', ascending=False)
    .reset_index(drop=True)
).round(2)
read_rate_df.index += 1

#Inbox Placement Ranking
inbox_df = (
    filtered_df.groupby('Company name')['overall_inbox_placement']
    .mean()
    .reset_index()
    .rename(columns={'overall_inbox_placement': 'Avg Inbox Placement (%)'})
    .sort_values('Avg Inbox Placement (%)', ascending=False)
    .reset_index(drop=True)
).round(2)
inbox_df.index += 1

col1, col2 = st.columns(2)
with col1:
    st.subheader(f'Read Rate — {selected_category}')
    st.dataframe(read_rate_df.rename_axis('Rank'))
with col2:
    st.subheader(f'Inbox Placement — {selected_category}')
    st.dataframe(inbox_df.rename_axis('Rank'))




st.markdown("---")
st.header("🔍 Insights & Recommendations")
st.caption("Based on qualitative audit of top-performing emails across 7 parameters: Subject Line, Design, Message Clarity, CTA, Personalization, Offer Proposition, Email Length")

with st.expander("📌 Subject Line Patterns", expanded=True):
    st.markdown("""
    - Emails using a specific data point, named speaker, or named event in the subject line outperform emails using a category or brand label alone, observed consistently in the Outlook and Webinar audit sets.
    - Newsletter brand names used as the entire subject line (e.g. "Macro Pulse: Decoding Market Trends," "Tathya June-2025") underperform subject lines that lead with the specific insight inside the newsletter.
    - Webinar subject lines combining a named speaker with a same-day time anchor (e.g. "Join Mr. Nilesh Shah at 4:00 PM Today!") are present across the highest-performing Kotak and SBI webinar emails in the audit set.
    - Milestone and occasion-based subject lines with name personalization (e.g. "Congratulations [Name], it's been 6 months!") recorded the two highest read rates in the Generic category audit (50% and 33.33%, both Axis).
    - Generic motivational or app-tagline subject lines with no specific hook (e.g. "Invest Smarter, Anytime, Anywhere!") recorded the lowest read rates in the Generic category audit.
    """)

with st.expander("📌 Design Patterns"):
    st.markdown("""
    - Emails where the key message is visible instantly, without requiring the reader to scroll, are present across the highest read rate entries in the Fund category audit.
    - Identical or near-identical creative templates reused across multiple Kotak SIP emails are present across a wide read rate range (5.56% to 50%), indicating that creative repetition alone does not determine read rate, the subject line and message framing applied to that same creative make the difference.
    - Data-dense, factsheet-style designs are present across the highest-performing ICICI Pru Outlook emails, indicating the MFD audience for this category engages with information density rather than being deterred by it.
    """)

with st.expander("📌 Message Clarity & CTA Patterns"):
    st.markdown("""
    - Emails with a single, specific, action-oriented CTA are present across the highest read rate entries in the Fund and SIP categories.
    - Emails with CTAs not clearly connected to the email's core hook or timing trigger (e.g. a SIP email mentioning salary-day timing but the CTA does not reference it) are present in the audit notes as a recurring observation across multiple Kotak SIP emails.
    - Multiple competing CTAs in a single email are present across several mid-to-low read rate entries in the Generic and Outlook categories.
    """)

with st.expander("📌 Personalization Patterns"):
    st.markdown("""
    - Name personalization combined with a behavioral or milestone trigger (SIP anniversaries, birthdays) is present across the two highest read rates in the entire Generic category audit, both from Axis (50% and 33.33%).
    - Kotak's SIP emails consistently carry name personalization across the audit set, but read rates within that set still range from 5.56% to 50%, indicating personalization alone does not determine read rate without an accompanying specific hook or trigger.
    - "Dear Partner" and "Dear Investor" generic salutations are present across the majority of Outlook and Webinar category emails across all AMCs in the audit set, including the highest-performing ICICI Pru entries, indicating this category's MFD audience responds primarily to content relevance rather than name-level personalization.
    """)

with st.expander("📌 Offer Proposition Patterns"):
    st.markdown("""
    - Emails communicating a specific, quantified data point or fact (a rating upgrade, a growth percentage, a specific statistic) as the core proposition are present across the highest read rates in the Outlook category, led by ICICI Pru's S&P ratings upgrade email at 55.56%.
    - NFO closing/urgency propositions are present across the highest read rates in the Fund category audit, including SBI's "Closing Soon" email at 60%, the highest single read rate recorded across the entire audit dataset.
    - Emails where the proposition requires the reader to open the email to understand the offer (no proposition stated upfront) are present across several lower read rate entries across the Webinar and Outlook categories.
    """)

with st.expander("📌 Email Length Patterns"):
    st.markdown("""
    - Short, single-card or single-screen emails are present across the highest read rates in the Webinar category across all four audited AMCs.
    - Long emails with multiple sections (Axis's Generic category emails, for example) are present across both high and low read rates within the same AMC, indicating length alone does not determine read rate independent of the content within those sections.
    - Information-dense, factsheet-style long emails are present across the highest-performing ICICI Pru Outlook entries, indicating that for the MFD-facing Outlook category specifically, length is not a deterrent when the content has practical utility.
    """)

st.markdown("---")
st.subheader("📌 Kotak: Consolidated Observations")

with st.expander("📝 Kotak Performance Summary", expanded=True):
    st.markdown("""
    Kotak underperforms the category leader across all email categories, indicating a consistent gap in engagement. The analysis highlights repetitive campaign creatives, inconsistent personalization, and weak or missing call-to-action elements in several emails. Additionally, content length and messaging often lack strategic alignment, reducing overall communication effectiveness. These findings suggest opportunities to improve campaign variety, personalization, and action-oriented messaging to enhance email performance.
    """)

with st.expander("📌 Kotak: Direct Recommendations"):
    st.markdown("""
    **1. Vary the Webinar email template instead of reusing the same design for every session.**
    Nearly every Kotak Webinar email uses the same red/white card layout with the same CTA wording across different speakers and topics, giving the audience no visual cue that a new session is being promoted.

    **2. Give every email a single, clear, action-tied CTA.**
    Several Fund and Generic emails either have no CTA, a CTA unrelated to the message, or list multiple reasons to act without the CTA tying back to any one of them — for example, an app-promotion email lists six separate features but the CTA ("Download our App") doesn't connect to any specific one of them.

    **3. Apply name personalization consistently across all categories, not just SIP.**
    Kotak's SIP emails consistently use name personalization, but Generic and Webinar emails largely use no personalization or a generic "Dear Partner" salutation — an inconsistency across categories sent to the same audience.

    **4. Make the investor benefit the lead message, not the fund or feature itself.**
    Several Fund emails are structured around the fund's name or internal features first, with the investor benefit appearing only after scrolling — a structure distinct from emails that put the reader's outcome in the first line.

    **5. Match email length to the complexity of the message.**
    Some SIP emails carry long supporting copy to communicate a single idea, while several Generic emails (festive greetings, "Happy New Year") carry no investment message at all — both are length-to-content mismatches in opposite directions.
    """)