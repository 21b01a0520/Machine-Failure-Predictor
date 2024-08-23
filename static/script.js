$(document).ready(function() {
    $('#predictForm').on('submit', function(e) {
        e.preventDefault();
        $.ajax({
            url: '/predict',
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                $('#result').html(
                    '<h4 class="animated-result">Prediction: ' + response.prediction + ' 🔧</h4>' +
                    '<p class="animated-result">Suggestion: ' + response.suggestion + ' 💡</p>'
                );
                $('.chart-container').show();
                renderChart(response.input_values, response.ideal_values);
            },
            error: function(error) {
                $('#result').html('<h4 class="animated-result">Error: ' + error.responseJSON.message + ' ❌</h4>');
            }
        });
    });

    function getAIAnalysis(prediction) {
        $.ajax({
            url: '/ai_analysis',
            type: 'POST',
            data: JSON.stringify({ prediction: prediction }),
            contentType: 'application/json',
            success: function(response) {
                $('#ai-result').html('<p class="animated-result">' + response.analysis + ' 🤖</p>');
                $('#ai-analysis').show();
            },
            error: function(error) {
                $('#ai-result').html('<p class="animated-result">Error fetching AI analysis. ❌</p>');
            }
        });
    }

    $('#ai-icon').on('click', function() {
        let prediction = $('#result').text().split('Prediction: ')[1]?.split(' 🔧')[0];
        if (prediction) {
            $('#ai-analysis').toggle();
            getAIAnalysis(prediction);
        } else {
            $('#ai-result').html('<p class="animated-result">Make a prediction first! 🔍</p>');
            $('#ai-analysis').toggle();
        }
    });

    function renderChart(inputValues, idealValues) {
        const ctx = document.getElementById('chart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Air Temperature', 'Process Temperature', 'Rotational Speed', 'Torque', 'Tool Wear'],
                datasets: [{
                    label: 'Input Values',
                    data: inputValues,
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1,
                    barThickness: 'flex'
                }, {
                    label: 'Ideal Values',
                    data: idealValues,
                    backgroundColor: 'rgba(75, 192, 192, 0.5)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                    barThickness: 'flex'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Input vs Ideal Parameter Values'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: '#4CAF50'
                        },
                        grid: {
                            display: false // Removes background lines
                        }
                    },
                    x: {
                        ticks: {
                            color: '#4CAF50'
                        },
                        grid: {
                            display: false // Removes background lines
                        }
                    }
                },
                layout: {
                    padding: {
                        left: 20,
                        right: 20,
                        top: 20,
                        bottom: 20
                    }
                },
                elements: {
                    bar: {
                        borderRadius: 5,
                        hoverBorderWidth: 3,
                        borderSkipped: 'bottom'
                    }
                },
                interaction: {
                    mode: 'nearest',
                    axis: 'x',
                    intersect: false
                }
            }
        });
    }
});
