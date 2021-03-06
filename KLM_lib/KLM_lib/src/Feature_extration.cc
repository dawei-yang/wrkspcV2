#include <algorithm>
#include <cmath>
#include <iostream>
#include <vector>


#include "TGraph.h"



#include "KLM_lib/Feature_extraction.hpp"
#include "KLM_lib/extract_gradient.hpp"
#include "KLM_lib/look_for_after_pulsing.hpp"





std::vector<int> get_x() {
	std::vector<int> ret;
	for (int i = 0; i < 128; i++)
	{
		ret.push_back(i);
	}
	return ret;
}

void Feature_extraction_read_file(TTree* tree, int ChannelNr, TFile* outFile) {




  KLM_Tree t1(tree);



	auto out_tree1 = [&] {
		outFile->cd();
		std::string branch_name = "features_" + std::to_string(ChannelNr);
		auto ret =   std::make_shared<TTree>(branch_name.c_str(), branch_name.c_str());
    ret->SetDirectory(outFile->GetDirectory("/"));
      return ret;
	}();
  auto out_tree = out_tree1.get();

	//out_tree->SetDirectory(outFile->GetDirectory());
	feature_branch counter_branch(out_tree, "counter");
	feature_branch branch_peak(out_tree, "peak");
  feature_branch branch_peak_gradient(out_tree, "peak_gradient");
	feature_branch branch_falling_edge(out_tree, "falling_edge");
	feature_branch branch_rising_edge(out_tree, "rising_edge");
	feature_branch branch_TOT(out_tree, "TOT");
	adc_count_branch<int> branch_adc(out_tree, "adc_counts");
	adc_count_branch<int> branch_adc_x(out_tree, "adc_x");
  adc_count_branch<int> branch_gradient(out_tree, "gradient");
	feature_branch branch_after_pulse(out_tree, "after_pulse");
  
  
  adc_count_branch<double> branch_gradient_a2(out_tree, "gradient_a2");
  feature_branch branch_peak_gradient_a2(out_tree, "peak_gradient_a2");

  adc_count_branch<double> branch_gradient_a4(out_tree, "gradient_a4");
  feature_branch branch_peak_gradient_a4(out_tree, "peak_gradient_a4");

  adc_count_branch<double> branch_gradient_a6(out_tree, "gradient_a6");
  feature_branch branch_peak_gradient_a6(out_tree, "peak_gradient_a6");
	branch_adc_x << get_x();

	for (int i = 0; i < tree->GetEntries() - 1; ++i) {


		t1.GetEntry(i);
		auto vec = to_vector(t1.ADC_counts[ChannelNr]);
		auto vec1 = filter_waveform(vec, 100);
		branch_peak << extract_peak(vec1);
		branch_falling_edge << extract_faling_edge(vec1, 202, 250);

		branch_rising_edge << extract_rising_edge(vec1, 200, 100);

		feature counter;
		counter.signal = i;
		counter.time = i;
		counter_branch << counter;

		branch_TOT << extract_time_over_threshold(vec1, 200, 250);
    branch_after_pulse<< look_for_after_pulsing(vec1);
    auto grad =  extract_gradient(vec1);
    branch_gradient << grad;
    branch_peak_gradient << extract_peak(grad);

    auto grad_a2 = extract_gradient_Accuracy2(vec1);
    branch_gradient_a2 << grad_a2;
    branch_peak_gradient_a2 << extract_peak(grad_a2);


    auto grad_a4 = extract_gradient_Accuracy4(vec1);
    branch_gradient_a4 << grad_a4;
    branch_peak_gradient_a4 << extract_peak(grad_a4);


    auto grad_a6 = extract_gradient_Accuracy6(vec1);
    branch_gradient_a6 << grad_a6;
    branch_peak_gradient_a6 << extract_peak(grad_a6);


		branch_adc << t1.ADC_counts[ChannelNr];
		out_tree->Fill();

	}

	

  out_tree->Write();


}


void Feature_extraction_read_file2(const std::string& fileName, const std::string& fileNameOut)
{
  TFile _file0(fileName.c_str());
	TFile out1(fileNameOut.c_str(), "RECREATE");
  auto tree = dynamic_cast<TTree*>(_file0.Get("tree"));
	Feature_extraction_read_file(tree, 14, &out1);
	Feature_extraction_read_file(tree, 0, &out1);
}
